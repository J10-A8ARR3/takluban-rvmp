from flask import Flask, request, jsonify
from flask_cors import CORS
from TAKLUBAN import predict_and_censor, get_pattern_generator
from tklbn_modules.FNLI.FNLI import LanguageIdentification, ModelTraining
import joblib
import os

app = Flask(__name__)
CORS(app)  # Allow requests from React frontend

# Paths
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "tklbn-modules", "FNLI", "saved_model.pkl")
DICTIONARY_DIR = os.path.join(BASE_DIR, "datasets", "FNLI-Dictionary")
SVM_MODEL_PATH = os.path.join(BASE_DIR, "trained_profane_model.pkl")

# Global variables for models
language_model = None
X_test, y_test = None, None
svm_model = None

def load_models():
    """Load models during app startup to prevent reloading in every request."""
    global language_model, X_test, y_test, svm_model

    if not language_model:
        if os.path.exists(MODEL_PATH):
            language_model = joblib.load(MODEL_PATH)
        else:
            trainer = ModelTraining(DICTIONARY_DIR)
            language_model, X_test, y_test = trainer.train_model()
            joblib.dump(language_model, MODEL_PATH)

    if not svm_model and os.path.exists(SVM_MODEL_PATH):
        svm_model = joblib.load(SVM_MODEL_PATH)

# Load models once at startup
with app.app_context():
    load_models()

@app.route('/detect_language', methods=['POST'])
def detect_language():
    """API to detect language, POS tagging, and censor profane words."""
    data = request.json  # Expecting JSON from React
    text = data.get("text", "").strip()

    if not text:
        return jsonify({'error': 'No input text provided'}), 400

    # Predict the language
    language_identifier = LanguageIdentification(model=language_model, X_test=X_test, y_test=y_test)
    predicted_language = language_identifier.predict_language(text)
    supported_languages = {'tagalog', 'bikol', 'cebuano'}

    if predicted_language not in supported_languages:
        return jsonify({
            'predicted_language': predicted_language,
            'error': f"'{predicted_language}' is not supported."
        }), 400

    # Get the pattern generator for the predicted language
    pattern_generator = get_pattern_generator(predicted_language)
    if not pattern_generator:
        return jsonify({
            'predicted_language': predicted_language,
            'error': f"Pattern generator for '{predicted_language}' not found."
        }), 400

    # Perform POS tagging and censorship
    pos_tagged_sentence = ' '.join(pattern_generator.tag_sentence(text))
    censored_sentence, is_profane = predict_and_censor(text, pattern_generator, svm_model, predicted_language)

    return jsonify({
        'predicted_language': predicted_language,
        'pos_tagged_sentence': pos_tagged_sentence,
        'censored_sentence': censored_sentence,
        'is_profane': is_profane
    }), 200

if __name__ == '__main__':
    app.run(debug=True)
