import os
import librosa
import numpy as np
import joblib
from flask import Flask, request, render_template, jsonify

app = Flask(__name__)

# Load pre-trained model (replace with your model)
# Example: a simple sklearn classifier trained on MFCC features
MODEL_PATH = "model.pkl"
model = joblib.load(MODEL_PATH) if os.path.exists(MODEL_PATH) else None

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    if "audio" not in request.files:
        return jsonify({"error": "No audio uploaded"}), 400

    audio_file = request.files["audio"]
    audio_path = "temp.wav"
    audio_file.save(audio_path)

    # Extract features (example: MFCCs)
    y, sr = librosa.load(audio_path, sr=16000)
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    features = np.mean(mfcc.T, axis=0).reshape(1, -1)

    if model:
        pred = model.predict(features)[0]
    else:
        pred = "demo: no model loaded"

    return jsonify({"prediction": str(pred)})

if __name__ == "__main__":
    app.run(debug=True)
