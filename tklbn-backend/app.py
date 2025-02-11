from flask import Flask, render_template, request, jsonify
from TAKLUBAN import predict_and_censor, get_pattern_generator
from tklbn_modules.FNLI.FNLI import LanguageIdentification, ModelTraining
import joblib

app = Flask(__name__)

# Paths and initialization
model_path = "../tklbn-backend/tklbn_modules/FNLI/saved_model.pkl"
dictionary_dir = "../tklbn-backend/datasets/FNLI-Dictionary"
svm_model_path = "trained_profane_model.pkl"

# Global variables for models
language_model = None
X_test, y_test = None, None
svm_model = None

def load_models():
    """Function to load models during app startup."""
    global language_model, X_test, y_test, svm_model

    # Load or train the language identification model
    if not language_model:
        trainer = ModelTraining(dictionary_dir)
        language_model, X_test, y_test = trainer.train_model()
        joblib.dump(language_model, model_path)
    else:
        language_model = joblib.load(model_path)

    # Load SVM model for profanity detection
    if not svm_model:
        svm_model = joblib.load(svm_model_path)

# Load models during app startup
with app.app_context():
    load_models()

# Routes for various pages
@app.route('/')
def home():
    """Render the Home page."""
    return render_template('Home.html')

@app.route('/index')
def index():
    """Render the Index page."""
    return render_template('index.html')

@app.route('/creators')
def creators():
    """Render the Creators page."""
    return render_template('Creators.html')

@app.route('/faqs')
def faqs():
    """Render the FAQs page."""
    return render_template('FAQs.html')

@app.route('/detect_language', methods=['POST'])
def detect_language():
    """API endpoint to detect language, perform POS tagging, and censor profane words."""
    text = request.form.get('text', '').strip()
    if not text:
        return jsonify({
            'error': 'No input text provided'
        })

    # Predict the language
    language_identifier = LanguageIdentification(model=language_model, X_test=X_test, y_test=y_test)
    predicted_language = language_identifier.predict_language(text)
    supported_languages = {'tagalog', 'bikol', 'cebuano'}

    if predicted_language not in supported_languages:
        return jsonify({
            'predicted_language': predicted_language,
            'error': f"The language '{predicted_language}' is not supported."
        })

    # Get the pattern generator for the predicted language
    pattern_generator = get_pattern_generator(predicted_language)
    if not pattern_generator:
        return jsonify({
            'predicted_language': predicted_language,
            'error': f"Pattern generator for '{predicted_language}' is not available."
        })

    # Perform POS tagging and censorship
    pos_tagged_sentence = ' '.join(pattern_generator.tag_sentence(text))
    censored_sentence, is_profane = predict_and_censor(text, pattern_generator, svm_model, predicted_language)

    return jsonify({
        'predicted_language': predicted_language,
        'pos_tagged_sentence': pos_tagged_sentence,
        'censored_sentence': censored_sentence,
        'is_profane': is_profane
    })

if __name__ == '__main__':
    app.run(debug=True)