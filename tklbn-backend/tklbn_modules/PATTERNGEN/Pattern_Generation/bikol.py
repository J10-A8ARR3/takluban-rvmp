import os
import pandas as pd
import csv
from nltk.tag.stanford import StanfordPOSTagger
from nltk.util import ngrams
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.pipeline import make_pipeline
from sklearn.metrics import classification_report
import joblib

class PatternGenerator:
    def __init__(self, csv_filename, model_filename, path_to_jar):
        self.rules = self.load_predefined_rules(csv_filename)
        self.tagger = StanfordPOSTagger(model_filename=model_filename, path_to_jar=path_to_jar)
    
    def load_predefined_rules(self, csv_filename):
        rules = []
        try:
            with open(csv_filename, 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    rules.append({
                        'Rule Name': row['Rule Name'],
                        'POS Pattern': row['POS Pattern'].split(),
                        'Description': row['Description']
                    })
        except Exception as e:
            print(f"Error loading rules from {csv_filename}: {e}")
        return rules
    
    def generate_ngrams(self, pos_tagged_text, n):
        # Reuse the POS extraction code
        pos_tags = [item.split('|')[-1] for item in pos_tagged_text if '|' in item]  # Extract POS tags only
        
        print(f"Extracted POS Tags: {pos_tags}")  # Debugging: Print extracted POS tags

        # Generate n-grams using the extracted POS tags
        ngrams_list = list(ngrams(pos_tags, n))
        print(f"Generated {n}-grams: {ngrams_list}")  # Debugging: Print generated n-grams
        return ngrams_list

    def apply_rules_to_ngrams(self, ngram_list):
        flagged_patterns = []
        matching_ngram_indices = []  # Store indices of the profane n-grams

        for idx, ngram in enumerate(ngram_list):
            print(f"Checking n-gram: {ngram}")  # Debugging: Output the generated n-gram

            for rule in self.rules:
                pattern = rule['POS Pattern']  # The POS Pattern is already a list of POS tags

                # Ensure the n-gram and pattern are of the same length before comparison
                if len(ngram) == len(pattern) and list(ngram) == pattern:
                    flagged_patterns.append(f"Rule Matched: {rule['Rule Name']} - {rule['Description']}")
                    matching_ngram_indices.append(idx)  # Store the index of the matched n-gram
                    print(f"Match found: {rule['Rule Name']}")  # Debugging

        return flagged_patterns, matching_ngram_indices

    def detect_profane_patterns(self, pos_tagged_text):
        results = []
        profane_ngram_indices = []  # Add this to track the indices of matched n-grams

        # Loop over n-gram lengths (1-gram, 2-gram, 3-gram)
        for n in range(1, 4):  # For 1-gram, 2-gram, 3-gram
            # Generate n-grams from the POS-tagged sentence
            ngrams_list = self.generate_ngrams(pos_tagged_text, n)

            # Apply the predefined rules to the generated n-grams
            detected_patterns, ngram_indices = self.apply_rules_to_ngrams(ngrams_list)

            # If patterns are detected, add them to the results and track the n-gram indices
            if detected_patterns:
                results += detected_patterns
                profane_ngram_indices += ngram_indices

        # Return the detected patterns and the indices of the profane n-grams
        return results if results else ["No profane patterns detected"], profane_ngram_indices

    def add_new_rule(self, csv_filename, rule_name, pos_pattern, description):
        current_rules = self.load_predefined_rules(csv_filename)
        for rule in current_rules:
            if rule['POS Pattern'] == pos_pattern.split():
                print(f"Rule '{rule_name}' with POS pattern '{pos_pattern}' already exists.")
                return
        
        new_rule = {
            'Rule Name': rule_name,
            'POS Pattern': pos_pattern,
            'Description': description
        }
        
        try:
            with open(csv_filename, 'a', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=['Rule Name', 'POS Pattern', 'Description'])
                if file.tell() == 0:
                    writer.writeheader()
                writer.writerow(new_rule)
                print(f"New rule '{rule_name}' added successfully.")
        except Exception as e:
            print(f"Error adding new rule to {csv_filename}: {e}")
    
    def tag_sentence(self, sentence):
        tokens = sentence.split()
        tagged_sentence = self.tagger.tag(tokens)
        return [f"{word}|{tag}" for word, tag in tagged_sentence]
 
    def save_patterns_from_sentence(self, csv_filename, sentence, description):
        pos_tagged_sentence = self.tag_sentence(sentence)
        
        print(f"POS-tagged Sentence: {pos_tagged_sentence}")
        
        try:
            pos_pattern = ' '.join([item.split('|')[-1] for item in pos_tagged_sentence if '|' in item])
            print(f"Extracted POS Pattern: {pos_pattern}")
            
        except IndexError:
            print("Error: Incorrect tagging format in sentence.")
            return

        rule_name = f"rule_from_sentence_{len(self.rules) + 1}"
        self.add_new_rule(csv_filename, rule_name, pos_pattern, description)
        print(f"New rule '{rule_name}' added with POS pattern: {pos_pattern}")

    # Censoring the sentence based on the detected profane pattern
    def censor_sentence(pos_tagged_sentence, profane_indices):
        return ' '.join(
            '*****' if idx in profane_indices else word.split('|')[0] for idx, word in enumerate(pos_tagged_sentence)
        )
    
def main():
    base_path = "../takluban-rvmp"
    predefined_rules_path = f"{base_path}/tklbn-backend/tklbn-modules/3-PATTERNGEN/Pattern_Generation/predefined_rules.csv"
    model_filename = '../POS/FSPOST/filipino-left5words-owlqn2-distsim-pref6-inf2.tagger'
    path_to_jar = '../POS/FSPOST/stanford-postagger-full-2020-11-17/stanford-postagger.jar'
    profane_dictionary_path = 'Pattern_Generation/profane_dictionary.csv'
    
    def load_profane_dictionary():
        profane_dict = {}
        try:
            with open(profane_dictionary_path, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) == 2:  # Ensure that we have exactly two columns (word and count)
                        word, count = row
                        profane_dict[word] = int(count)
                    else:
                        print(f"Skipping invalid row in dictionary: {row}")
        except FileNotFoundError:
            print(f"{profane_dictionary_path} not found. A new dictionary will be created.")
        except Exception as e:
            print(f"Error loading profane dictionary: {e}")
        return profane_dict
    
    def predict_and_censor(sentence, best_model):
        is_profane = best_model.predict([sentence])[0]  # Prediction
        print(f"Is sentence profane?: {is_profane}")
        
        if not is_profane:
            return sentence  # If the sentence is not profane, return it as is
        
        pos_tagged_sentence = pattern_generator.tag_sentence(sentence)
        print("POS-tagged Sentence:", pos_tagged_sentence)  
        
        detected_patterns, profane_ngram_indices = pattern_generator.detect_profane_patterns(pos_tagged_sentence)
        print("Detected Patterns:", detected_patterns) 
        
        if "No profane patterns detected" in detected_patterns:
            return sentence  # No patterns detected, return original sentence
        
        # ** Save detected POS patterns to the dictionary **
        pos_patterns = [pattern.split(' - ')[0] for pattern in detected_patterns if 'Rule Matched' in pattern]
        save_profane_to_dict(pos_patterns)  # Save detected POS patterns
        
        # Loop through the pos_tagged_sentence and censor only the detected profane words
        censored_sentence = []
        ngram_size = len(profane_ngram_indices)  # Size of the n-grams we are censoring
        profane_word_indices = []

        # Generate n-grams based on the POS-tagged sentence
        pos_tags = [item.split('|')[-1] for item in pos_tagged_sentence if '|' in item]
        words = [item.split('|')[1] for item in pos_tagged_sentence if '|' in item]

        # Identify the word indices to censor based on profane n-grams
        for idx in profane_ngram_indices:
            profane_word_indices.extend(range(idx, idx + ngram_size))  # Get all word indices in the profane n-gram

        # Censor the words at the profane indices
        for idx, word in enumerate(words):
            if idx in profane_word_indices:
                censored_sentence.append('*****')  # Censor this word
            else:
                censored_sentence.append(word)  # Keep the word as is
        
        return ' '.join(censored_sentence)

    # Function to save the profane dictionary to CSV
    def save_profane_dictionary(profane_dict):
        try:
            with open(profane_dictionary_path, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                for word, count in profane_dict.items():
                    writer.writerow([word, count])
            print(f"Profane dictionary saved successfully to {profane_dictionary_path}.")
        except Exception as e:
            print(f"Error saving profane dictionary: {e}")

    # Function to update and save detected POS patterns to the CSV
    def save_profane_to_dict(pos_patterns):
        # Load existing profane dictionary from the CSV file
        profane_dict = load_profane_dictionary()

        # Update the dictionary with new POS patterns
        for pattern in pos_patterns:
            if pattern in profane_dict:
                profane_dict[pattern] += 1  # Increment the count if pattern already exists
            else:
                profane_dict[pattern] = 1  # Add new pattern

        # Save the updated profane dictionary back to the CSV file
        save_profane_dictionary(profane_dict)
        print(f"Updated Profane Dictionary with POS Patterns: {profane_dict}")

    pattern_generator = PatternGenerator(predefined_rules_path, model_filename, path_to_jar)
    
    # Define the sentence to test
    sentence = "lintian na gibuhon ini"
        
    # Save pattern from the sentence
    pattern_generator.save_patterns_from_sentence(predefined_rules_path, sentence, "Profane sentence example")
    
    # Load your dataset
    df = pd.read_csv('../takluban-rvmp/tklbn-backend/datasets/RAW/dataset_bikol.csv')
    
    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(df['sentence'], df['profane'], test_size=0.5, random_state=48)
    
    # Create a pipeline that combines the TfidfVectorizer with N-Grams and SVM
    pipeline = make_pipeline(TfidfVectorizer(ngram_range=(1, 2)), SVC())
    
    # Define the hyperparameters grid
    param_grid = {
        'svc__C': [0.1, 1, 10],
        'svc__kernel': ['linear', 'rbf']
    }
    
    # Perform Grid Search with Cross-Validation
    grid_search = GridSearchCV(pipeline, param_grid, cv=5, scoring='accuracy')
    grid_search.fit(X_train, y_train)
    
    # Best model from grid search
    best_model = grid_search.best_estimator_
    
    # Evaluate the model
    y_pred = best_model.predict(X_test)
    print(classification_report(y_test, y_pred))

    # Example usage
    prediction = predict_and_censor(sentence, best_model)
    print(f"Output: {prediction}")

    pos_tagged_sentence = pattern_generator.tag_sentence(sentence)
    print("POS-tagged Sentence:", pos_tagged_sentence)

    detected_patterns = pattern_generator.detect_profane_patterns(pos_tagged_sentence)
    print("Detected Patterns:", detected_patterns)

    censored_sentence = predict_and_censor(sentence, best_model)
    print(f"Output: {censored_sentence}")

if __name__ == "__main__":
    main()