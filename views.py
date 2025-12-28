from flask import Blueprint, jsonify

# Define the blueprint
# 'api' is the internal name Flask uses
api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/', methods=['GET'])
def hello():
    return jsonify({'message': 'Hello, world!'}), 200