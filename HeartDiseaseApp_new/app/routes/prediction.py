from flask import Blueprint, request, jsonify
from app.utils.preprocess import preprocess_data
import pickle

prediction_bp = Blueprint("prediction", __name__)

# Load pre-trained models
models = {
    "knn": pickle.load(open("app/models/knn_model.pkl", "rb")),
    "random_forest": pickle.load(open("app/models/random_forest_model.pkl", "rb")),
}

@prediction_bp.route("/", methods=["POST"])
def predict():
    data = request.json
    processed_data = preprocess_data(data)
    predictions = {name: int(model.predict([processed_data])[0]) for name, model in models.items()}
    return jsonify(predictions)
