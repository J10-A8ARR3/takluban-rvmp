import os
import re
from nltk.tag.stanford import StanfordPOSTagger

class StanfordPOSTaggerWrapper:
    def __init__(self):
        base_path = "TAKLUBAN-FILIPINO-NATIVE-LANGUAGE-PROFANE-DETECTION"
        self.model_path = "Modules/FSPOST/filipino-left5words-owlqn2-distsim-pref6-inf2.tagger"
        self.jar_path = "Modules/FSPOST/stanford-postagger-full-2020-11-17/stanford-postagger.jar"

        # Initialize the Stanford POS Tagger with Java heap optimization
        self.tagger = StanfordPOSTagger(
            model_filename=self.model_path,
            path_to_jar=self.jar_path,
            java_options="-mx6144m"  # Allocating 6GB memory
        )

    def pos_tag_text(self, text, language):
        """Performs POS tagging and applies Cebuano/Bikol rules if applicable."""
        tokens = text.split()
        pos_tags = self.tagger.tag(tokens)
        
        # Apply language-specific rules if applicable
        processed_tags = [self.language_rules(f"{word}|{tag}", language) for word, tag in pos_tags]
        return ' '.join(processed_tags)

    def clean_token(self, token):
        """Cleans and normalizes tokens."""
        return token.strip().lower()

    def language_rules(self, token, language):
        """Applies Cebuano or Bikol-specific POS tagging rules."""
        token = self.clean_token(token)

        # Cebuano rules
        if language == 'cebuano':
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
        # Bikol rules
        elif language == 'bikol':
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
        else:
            return token  # If not Cebuano or Bikol, return as-is

        try:
            word, current_tag = token.split('|')
        except ValueError:
            return token  # Return as-is if formatting is wrong

        for tag, pattern in patterns.items():
            if re.fullmatch(pattern, word, flags=re.IGNORECASE):
                print(f"Matched: {word} -> {tag}")  # Debugging output
                return f"{word}|{tag}"

        return token

if __name__ == "__main__":
    pos_tagger = StanfordPOSTaggerWrapper()
    
    while True:
        language = input("\nEnter language (cebuano/bikol or 'exit' to quit): ").strip().lower()
        if language == "exit":
            break
        if language not in ["cebuano", "bikol"]:
            print("Unsupported language. Please enter 'cebuano' or 'bikol'.")
            continue

        user_text = input("Enter text to POS tag: ")
        tagged_output = pos_tagger.pos_tag_text(user_text, language)
        print("\nPOS-Tagged Output:\n", tagged_output)
