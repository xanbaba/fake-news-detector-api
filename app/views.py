from flask import Blueprint, jsonify, request
from app.services.ml_model import get_newsletter_text, predict
from app.auth import firebase_auth_required

# Define the blueprint
# 'api' is the internal name Flask uses
api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/predict', methods=['GET'])
@firebase_auth_required
def predict_route():
    url = request.args.get("url", default='', type=str)
    if not url:
        return jsonify({"error": "`url` parameter is required"}), 400

    input_text = get_newsletter_text(url)
    prediction = predict(input_text)
    return jsonify({"prediction": prediction.name}), 200