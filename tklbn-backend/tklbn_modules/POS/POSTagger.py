import os
import pandas as pd
import re
from nltk.tag.stanford import StanfordPOSTagger

class StanfordPOSTaggerWrapper:
    def __init__(self, language):
        base_path = "../takluban-rvmp"
        results_folder = f"{base_path}/datasets/OUTPUT"
        self.input_file = f"{base_path}/tklbn-backend/datasets/RAW/preprocessed_{language}.csv"
        self.output_dir = results_folder
        self.output_file = f"{self.output_dir}/Tagged_{language}.csv"

        # Ensure the output directory exists
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        # Load the preprocessed data
        self.data = pd.read_csv(self.input_file, names=['sentence', 'label'])  # Assume 'sentence' and 'label' columns
        print(f"Loaded preprocessed data for {language}. Number of sentences: {len(self.data)}")

        # Set up the Stanford POS Tagger with increased memory allocation to 6 GB
        self.tagger = StanfordPOSTagger(
            model_filename='POS/FSPOST/filipino-left5words-owlqn2-distsim-pref6-inf2.tagger',
            path_to_jar='POS/FSPOST/stanford-postagger-full-2020-11-17/stanford-postagger.jar',
            java_options='-mx6144m'  # Set maximum Java heap size to 6 GB
        )

    def pos_tag_text(self, text):
        try:
            tokens = text.split()
            pos_tags = self.tagger.tag(tokens)
            pos_tagged_text = ' '.join([f"{word}|{tag}" for word, tag in pos_tags])  # Use word|tag format

            # Show the process of tagging each token
            for word, tag in pos_tags:
                print(f"Processed: {word} -> {tag}")

            return pos_tagged_text
        except Exception as e:
            print(f"Error during POS tagging: {e}")
            return text

    def pos_tag_sentences(self, batch_size=10):
        try:
            for i in range(0, len(self.data), batch_size):
                batch = self.data.iloc[i:i+batch_size].copy()  # Copy the batch to avoid warnings
                batch.loc[:, 'pos_tagged'] = batch['sentence'].apply(self.pos_tag_text)  # Tag each sentence

                # Save tagged sentences
                batch[['pos_tagged', 'label']].to_csv(self.output_file, mode='a', index=False, header=(i == 0))
                print(f"Processed batch {i//batch_size + 1} of {len(self.data) // batch_size + 1}")
            
            print(f"POS tagging complete. Results saved to {self.output_file}.")
        except Exception as e:
            print(f"An error occurred during POS tagging: {e}")


class POSTagger:
    def __init__(self, language):
        self.language = language.lower()
        self.output_file = '../takluban-rvmp/tklbn-backend/datasets/OUTPUT/POSdata.csv'

        # Ensure the output directory exists
        output_dir = os.path.dirname(self.output_file)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Initialize StanfordPOSTaggerWrapper for all languages
        if self.language in ['tagalog', 'cebuano', 'bikol']:
            self.stanford_tagger = StanfordPOSTaggerWrapper(language)

    def clean_token(self, token):
        token = token.strip()

        # Remove leading '/' if present before the word
        if token.startswith('/'):
            token = token[1:]

        # Ensure proper formatting of 'word|tag'
        if '|' not in token:
            print(f"Invalid token format, no '|': {token}")
            return token  # Return as-is if formatting is wrong

        word, tag = token.split('|', 1)  # Split only once at '|'
        word = word.strip()  # Clean up spaces around the word
        tag = tag.strip()  # Clean up spaces around the tag

        return f"{word}|{tag}"

    def language_rules(self, token):
        token = self.clean_token(token)

        if self.language == 'cebuano':
            patterns = {
                'VB': r'\b(mag|nag|mi|mo|mu|mang|manag|man)[a-zA-Z]+\b',  # Cebuano verb markers
                'NNC': r'\b([a-zA-Z]+on|[a-zA-Z]+an)\b',  # Cebuano nouns
                'NNCA': r'\b(ka|pang)[a-zA-Z]+an\b',  # Cebuano affix nouns
                'NNPL': r'\bmga\s+[a-zA-Z]+\b',  # Plural nouns prefixed by "mga"
                'JJD': r'\b(ma|ka)[a-zA-Z]+an\b',  # Cebuano adjectives
                'JJCM': r'\bmas\s+[a-zA-Z]+\b',  # Comparative adjectives
                'PRP': r'\bako|ikaw|siya|kami|kita|sila\b',  # Cebuano pronouns
                'DT': r'\bang|bang|mga\b',  # Cebuano determiners
                'CCP': r'\bug|o|kundi\b',  # Cebuano conjunctions
            }
        elif self.language == 'bikol':
            patterns = {
                'VB': r'\b(MA|MAG|NAG|MANG|PINAG|PA|KA)[a-zA-Z]+\b',  # Bikol verb markers
                'NN': r'\b[a-zA-Z]+on\b|\b[a-zA-Z]+an\b|\b[a-zA-Z]+(TA|HON|LAY|LI)[a-zA-Z]*\b',  # Bikol nouns
                'JJ': r'\b(A|KA|MALA)[a-zA-Z]+on\b|\bPINAKA[a-zA-Z]+\b',  # Bikol adjectives
                'PRP': r'\bAKO|IKAW|SIYA|KAMI|KITA|SINDA|NIYA|NINDA|NIATO|NATO|SAINDO\b',  # Bikol pronouns
                'DT': r'\bANG|MGA|SI|SA|KAN|KUN\b',  # Bikol determiners
                'RB': r'\b(DAKUL|GAD|HALA|DAI|MAYA|SIRA|SINYA|URUG)\b',  # Bikol adverbs
                'CC': r'\bOG|PERO|KUNDI\b',  # Conjunctions
                'IN': r'\bPARA|PAAGI|ASIN|KAN\b',  # Prepositions
                'CD': r'\bSARO|DUWA|TULO|APAT|LIMA|ANOM|PITO|WALO|SIYAM|SAMPULO\b',  # Numbers
            }

        try:
            word, current_tag = token.split('|')
        except ValueError:
            return token  # Return as-is if formatting is wrong

        for tag, pattern in patterns.items():
            if re.fullmatch(pattern, word, flags=re.IGNORECASE):
                print(f"Matched: {word} -> {tag}")
                return f"{word}|{tag}"

        return token

    def pos_tag_text(self, text):
        # Use Stanford POS tagging for all languages first
        stanford_tagged_text = self.stanford_tagger.pos_tag_text(text)
        print(f"Stanford tagged text: {stanford_tagged_text}")

        # If not Tagalog, apply language-specific rules after Stanford POS tagging
        if self.language in ['cebuano', 'bikol']:
            tokens = stanford_tagged_text.split()
            pos_tagged_tokens = [self.language_rules(token) for token in tokens]
            return ' '.join(pos_tagged_tokens)
        else:
            return stanford_tagged_text

    def pos_tag_input(self, user_text):
        pos_tagged_text = self.pos_tag_text(user_text)

        # Save the tagged text to the CSV file
        with open(self.output_file, 'a') as f:
            f.write(f"{user_text},{pos_tagged_text}\n")

        print(f"POS tagged text saved to {self.output_file}")


if __name__ == "__main__":
    language = input("Enter the language to process (cebuano/bikol/tagalog): ").lower()

    if language not in ['cebuano', 'bikol', 'tagalog']:
        print(f"Unsupported language: {language}")
    else:
        pos_tagger = POSTagger(language)
        user_text = input("Enter the text you want to POS tag: ")
        pos_tagger.pos_tag_input(user_text)