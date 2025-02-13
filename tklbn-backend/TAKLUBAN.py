import csv
import os
import pandas as pd
import joblib
from sklearn.metrics import confusion_matrix, classification_report
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import re
from tklbn_modules.FNLI.FNLI import LanguageIdentification, ModelTraining
from tklbn_modules.PATTERNGEN.Pattern_Generation.tagalog import PatternGenerator as TagalogPatternGenerator
from tklbn_modules.PATTERNGEN.Pattern_Generation.bikol import PatternGenerator as BikolPatternGenerator
from tklbn_modules.PATTERNGEN.Pattern_Generation.cebuano import PatternGenerator as CebuanoPatternGenerator

# Define directories and file paths
output_dir = "../takluban-rvmp/tklbn-backend/datasets/OUTPUT"
os.makedirs(output_dir, exist_ok=True)
output_file = os.path.join(output_dir, "POSdata.csv")

profanity_dictionary_dir = "../takluban-rvmp/tklbn-backend/tklbn_modules/PATTERNGEN/Pattern_Generation"
os.makedirs(profanity_dictionary_dir, exist_ok=True)
profanity_dictionary_file = os.path.join(profanity_dictionary_dir, "profane_dictionary.csv")

# Initialize CSV files if they do not exist
if not os.path.exists(output_file):
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Language', 'Sentence', 'POS', 'Censored Sentence'])

if not os.path.exists(profanity_dictionary_file):
    with open(profanity_dictionary_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Language', 'Profane Sentence'])

predictions = []
true_labels = []

# Define noise words
noise_words = {...}  # Same noise words as before

def save_to_csv(language, sentence, pos_tagged, censored_sentence):
    with open(output_file, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([language, sentence, pos_tagged, censored_sentence])

def save_profane_pattern(language, sentence, pos_pattern):
    with open(profanity_dictionary_file, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([language, sentence, pos_pattern])

def train_model_if_not_exists(model_path, dictionary_dir):
    if not os.path.exists(model_path):
        print(f"Model file {model_path} not found. Training a new model...")
        trainer = ModelTraining(dictionary_dir)
        model, X_test, y_test = trainer.train_model()
        joblib.dump(model, model_path)
        print(f"Model trained and saved at {model_path}.")
        return model, X_test, y_test
    else:
        print(f"Loading pre-saved model from {model_path}.")
        model = joblib.load(model_path)
        return model, [], []

def get_pattern_generator(language):
    predefined_rules_path = os.path.join(profanity_dictionary_dir, "predefined_rules.csv")
    model_filename = '../takluban-rvmp/tklbn-backend/tklbn_modules/POS/FSPOST/filipino-left5words-owlqn2-distsim-pref6-inf2.tagger'
    path_to_jar = '../takluban-rvmp/tklbn-backend/tklbn_modules/POS/FSPOST/stanford-postagger-full-2020-11-17/stanford-postagger.jar'
    
    if language == 'tagalog':
        return TagalogPatternGenerator(predefined_rules_path, model_filename, path_to_jar)
    elif language == 'bikol':
        return BikolPatternGenerator(predefined_rules_path, model_filename, path_to_jar)
    elif language == 'cebuano': 
        return CebuanoPatternGenerator(predefined_rules_path, model_filename, path_to_jar)
    return None

def predict_and_censor(sentence, pattern_generator, model, language):
    pos_tagged_sentence = pattern_generator.tag_sentence(sentence)
    tokens = sentence.split()
    filtered_tokens = [token for token in tokens if token.lower() not in noise_words]
    if not filtered_tokens:
        return sentence, False
    
    censored_tokens = []
    is_profane = False
    for token in tokens:
        if token.lower() in noise_words:
            censored_tokens.append(token)
        else:
            if model.predict([token])[0] == 1:
                censored_tokens.append(re.sub(r'\w', '*', token))
                is_profane = True
            else:
                censored_tokens.append(token)
    
    censored_sentence = ' '.join(censored_tokens)
    if is_profane:
        pos_pattern = ' '.join([item.split('\n')[-1] for item in pos_tagged_sentence if '\n' in item])
        save_profane_pattern(language, sentence, pos_pattern)
    return censored_sentence, is_profane

def display_output(language, sentence, pos_tagged, censored_sentence, is_profane):
    print(f"\nDetected Language: {language}")
    print(f"Original Sentence: {sentence}")
    print(f"POS Tagged Sentence: {pos_tagged}")
    print(f"Censored Sentence: {censored_sentence} ({'Profane' if is_profane else 'Not Profane'})")

def main():
    model_path = "../takluban-rvmp/tklbn-backend/tklbn_modules/FNLI/saved_model.pkl"
    dictionary_dir = "../takluban-rvmp/tklbn-backend/datasets/FNLI-Dictionary"
    model, X_test, y_test = train_model_if_not_exists(model_path, dictionary_dir)
    language_identifier = LanguageIdentification(model=model, X_test=X_test, y_test=y_test)
    supported_languages = {'tagalog', 'bikol', 'cebuano'}
    svm_model = joblib.load("../takluban-rvmp/tklbn-backend/trained_profane_model.pkl")
    
    while True:
        sentence = input("Enter a sentence (or type 'exit' to quit): ").strip()
        if sentence.lower() == 'exit':
            print("Exiting the program.")
            break
        
        predicted_language = language_identifier.predict_language(sentence)
        if predicted_language not in supported_languages:
            print(f"Detected language: {predicted_language}. This language is not supported.")
            continue
        
        pattern_generator = get_pattern_generator(predicted_language)
        if pattern_generator:
            pos_tagged = ' '.join(pattern_generator.tag_sentence(sentence))
            censored_sentence, is_profane = predict_and_censor(sentence, pattern_generator, svm_model, predicted_language)
            save_to_csv(predicted_language, sentence, pos_tagged, censored_sentence)
            display_output(predicted_language, sentence, pos_tagged, censored_sentence, is_profane)
    
if __name__ == "__main__":
    main()
