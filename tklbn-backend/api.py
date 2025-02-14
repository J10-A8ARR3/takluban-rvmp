from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import os
from TAKLUBAN import get_pattern_generator, predict_and_censor, train_model_if_not_exists
from tklbn_modules.FNLI.FNLI import LanguageIdentification

app = Flask(__name__)
CORS(app)  # Allow React frontend to make requests

# Load trained models
model_path = "../tklbn-backend/tklbn_modules/FNLI/saved_model.pkl"
dictionary_dir = "../tklbn-backend/datasets/FNLI-Dictionary"
svm_model_path = "../tklbn-backend/trained_profane_model.pkl"

model, X_test, y_test = train_model_if_not_exists(model_path, dictionary_dir)
language_identifier = LanguageIdentification(model=model, X_test=X_test, y_test=y_test)
svm_model = joblib.load(svm_model_path)

@app.route('/detect_language', methods=['POST'])
def detect_language():
    data = request.json
    sentence = data.get("sentence", "").strip()

    if not sentence:
        return jsonify({"error": "No sentence provided"}), 400

    predicted_language = language_identifier.predict_language(sentence)
    pattern_generator = get_pattern_generator(predicted_language)

    if pattern_generator:
        pos_tagged = ' '.join(pattern_generator.tag_sentence(sentence))
        censored_sentence, is_profane = predict_and_censor(sentence, pattern_generator, svm_model, predicted_language)
        return jsonify({
            "language": predicted_language,
            "pos_tagged": pos_tagged,
            "censored_sentence": censored_sentence,
            "is_profane": is_profane
        })
    else:
        return jsonify({"error": "Pattern generator not available for detected language"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)  # Run API on port 5000
