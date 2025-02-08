import os
import csv
import joblib
import subprocess
from collections import Counter
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

class DictionaryGenerator:
    def __init__(self, preprocessed_dir, dictionary_dir, english_dict_path, language):
        base_path = "../takluban-rvmp"
        results_folder = f"{base_path}/tklbn-backend/datasets"
        self.language = language  
        self.input_file = f"{results_folder}/RAW/preprocessed_{language}.csv"
        self.output_file = f"{results_folder}/RAW/preprocessed_{language}.csv"
        self.english_dict_path = f"{dictionary_dir}/english_dictionary.csv"
        self.preprocessed_dir = preprocessed_dir  # Ensure the directory paths are available
        self.dictionary_dir = dictionary_dir
        os.makedirs(os.path.dirname(self.output_file), exist_ok=True)

        # Initialize noise words for all languages
        self.noise_words = self.initialize_noise_words()

    def initialize_noise_words(self):
        """Initialize common noise words for Tagalog, Bikol, Cebuano, and English."""
        noise_words = {
            'Tagalog': {"nang", "mga", "kung", "yan", "ko", "po"},
            'Bikol': {"ngani",  "kang", "iyo", "hali", "baga", "ho", "mo", "na"},
            'Cebuano': {"dayon", "gani", "kana", "mao", "pud", "bitaw"}
        }
        noise_words['English'] = self.load_english_noise_words()

        # Clean the English noise words by removing common words in the three languages
        self.clean_english_noise_words(noise_words)

        return noise_words

    def load_english_noise_words(self):
        noise_words = set()
        try:
            with open(self.english_dict_path, 'r', encoding='utf-8') as infile:
                reader = csv.reader(infile)
                next(reader)  # Skip header
                for row in reader:
                    if row:  # Check if the row is not empty
                        word = row[0].strip()
                        noise_words.add(word.lower())
            print(f"Loaded {len(noise_words)} English noise words.")  # Debugging line
        except FileNotFoundError:
            print(f"Error: The file {self.english_dict_path} does not exist.")
        except Exception as e:
            print(f"An error occurred: {e}")
        return noise_words

    def clean_english_noise_words(self, noise_words):
        """Remove words from English noise words that exist in any of the other three language dictionaries."""
        tagalog_set = noise_words.get('Tagalog', set())
        bikol_set = noise_words.get('Bikol', set())
        cebuano_set = noise_words.get('Cebuano', set())

        # Find common words in the three languages and English, then remove them from English
        common_words = (tagalog_set | bikol_set | cebuano_set) & noise_words['English']
        noise_words['English'] = noise_words['English'] - common_words

    def remove_noise(self, words, language):
        """Remove noise words from the list of words."""
        return [word for word in words if word.lower() not in self.noise_words[language.capitalize()]]

    def generate_dictionary(self, language):
        """Generate a word frequency dictionary from preprocessed sentences, excluding words found in the English dictionary."""
        word_count = Counter()
        preprocessed_file = os.path.join(self.preprocessed_dir, f"preprocessed_{language}.csv") # Fix the error here

        try:
            with open(preprocessed_file, 'r', encoding='utf-8') as infile:
                reader = csv.reader(infile)
                for row in reader:
                    if row:  # Check if the row is not empty
                        sentence = row[0]
                        words = sentence.split()
                        # Remove noise words and English words before counting
                        cleaned_words = [word for word in self.remove_noise(words, language)
                                         if word.lower() not in self.noise_words['English']]
                        word_count.update(cleaned_words)

            # Save the dictionary
            self.save_dictionary(word_count, language)

        except FileNotFoundError:
            print(f"Error: The file {preprocessed_file} does not exist.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def save_dictionary(self, word_count, language):
        """Save the word frequency dictionary to a CSV file."""
        dict_file = os.path.join(self.dictionary_dir, f"{language}_dictionary.csv")
        with open(dict_file, 'w', newline='', encoding='utf-8') as dict_file:
            writer = csv.writer(dict_file)
            writer.writerow(['word', 'frequency'])
            for word, freq in sorted(word_count.items()):
                writer.writerow([word, freq])
        print(f"Dictionary saved at {dict_file}")

class ModelTraining:
    """This class is responsible for training the language identification model."""
    
    def __init__(self, dictionary_dir):
        self.dictionary_dir = dictionary_dir
        self.word_frequencies = self.load_dictionaries()

    def load_dictionaries(self):
        frequencies = {}
        for language in ['tagalog', 'bikol', 'cebuano']:
            dict_file = os.path.join(self.dictionary_dir, f"{language}_dictionary.csv")
            if os.path.exists(dict_file):
                df = pd.read_csv(dict_file)
                frequencies[language] = dict(zip(df['word'], df['frequency']))
                print(f"Loaded {language} dictionary with {len(frequencies[language])} entries.")
            else:
                print(f"Dictionary file for {language} not found.")
        return frequencies

    def train_model(self):
        # Prepare training data
        data = []
        labels = []
        for language, word_freq in self.word_frequencies.items():
            for word, freq in word_freq.items():
                if freq > 0 and isinstance(word, str):  # Check for positive frequency and valid word
                    data.extend([word] * freq)
                    labels.extend([language] * freq)

        # Check for empty data or labels
        if not data or not labels:
            raise ValueError("Training data or labels are empty. Please check your dictionary files.")

        # Split the data (60% training, 30% validation, 10% testing)
        X_train, X_temp, y_train, y_temp = train_test_split(data, labels, test_size=0.40, random_state=50)
        X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.25, random_state=50)  # 0.25 * 0.40 = 0.10

        print(f"Train size: {len(X_train)}, Validation size: {len(X_val)}, Test size: {len(X_test)}")

        # Create a pipeline with TfidfVectorizer for N-gram extraction and MultinomialNB with Laplace smoothing
        pipeline = make_pipeline(TfidfVectorizer(ngram_range=(1, 3)), MultinomialNB(alpha=1.0))

        # Hyperparameter tuning using GridSearchCV
        param_grid = {
            'tfidfvectorizer__ngram_range': [(1, 1), (1, 2), (1, 3)],
            'multinomialnb__alpha': [0.1, 0.5, 1.0]  # Laplace smoothing parameters
        }
        grid_search = GridSearchCV(pipeline, param_grid, cv=5, scoring='accuracy')
        grid_search.fit(X_train, y_train)

        model = grid_search.best_estimator_
        model.fit(X_train, y_train)

        # Save the trained model to a file
        model_path = "../takluban-rvmp/tklbn-backend/tklbn-modules/FNLI/saved_model.pkl"
        joblib.dump(model, model_path)  # Save the model to a .pkl file
        print(f"Model saved at {model_path}")

        return model, X_test, y_test

class LanguageIdentification:
    """This class is responsible for predicting the language based on a pre-trained model."""
    
    def __init__(self, model, X_test, y_test):
        self.model = model
        self.X_test = X_test
        self.y_test = y_test

    def predict_language(self, sentence):
        return self.model.predict([sentence])[0]

    def determine_language(self, sentences):
        language_counter = Counter()
        for sentence in sentences:
            dominant_language = self.predict_language(sentence)
            language_counter[dominant_language] += 1
        return language_counter.most_common(1)[0][0] if language_counter else None

    def evaluate_model(self):
        """Evaluate the model and calculate accuracy, precision, recall, and F1 score."""
        predictions = [self.predict_language(sentence) for sentence in self.X_test]

        # Calculate metrics
        accuracy = accuracy_score(self.y_test, predictions)
        precision = precision_score(self.y_test, predictions, average='weighted', zero_division=0)
        recall = recall_score(self.y_test, predictions, average='weighted', zero_division=0)
        f1 = f1_score(self.y_test, predictions, average='weighted', zero_division=0)

        return accuracy, precision, recall, f1

def run_preprocessing(preprocess_script):
    """Function to run the preprocessing script."""
    try:
        # Using subprocess to run the preprocessing script
        subprocess.run(["python", preprocess_script], check=True)
        print("Preprocessing completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running the preprocessing: {e}")
    except FileNotFoundError:
        print("Error: preprocess.py file not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    # Run preprocessing first
    preprocess_script = "../takluban-rvmp/tklbn-backend/tklbn-modules/FNLI/preProcess.py"
    run_preprocessing(preprocess_script)

    # Proceed with dictionary generation
    preprocessed_dir = "../takluban-rvmp/tklbn-backend/datasets/RAW"
    dictionary_dir = "../takluban-rvmp/tklbn-backend/datasets/FNLI-Dictionary"
    english_dict_path = "../takluban-rvmp/tklbn-backend/datasets/FNLI-Dictionary/english_dictionary.csv"

    languages = ['tagalog', 'bikol', 'cebuano']

    for language in languages:
        generator = DictionaryGenerator(preprocessed_dir, dictionary_dir, english_dict_path, language)
        generator.generate_dictionary(language)

    # Train the model
    trainer = ModelTraining(dictionary_dir)
    model, X_test, y_test = trainer.train_model()

    # Language identification using the trained model
    language_identifier = LanguageIdentification(model, X_test, y_test)

    # Evaluate the model
    accuracy, precision, recall, f1 = language_identifier.evaluate_model()
    print(f"Model Evaluation Metrics on Test Set:\n"
          f"Accuracy: {accuracy:.2f}\n"
          f"Precision: {precision:.2f}\n"
          f"Recall: {recall:.2f}\n"
          f"F1 Score: {f1:.2f}")

    # Command-line input for language identification
    while True:
        user_input = input("\nEnter a sentence to identify its language (or type 'exit' to quit): ").strip()
        if user_input.lower() == 'exit':
            print("Exiting the program. Goodbye!")
            break
        predicted_language = language_identifier.predict_language(user_input)
        print(f"Predicted Language: {predicted_language.capitalize()}")