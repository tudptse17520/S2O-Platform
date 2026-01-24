from flask import Blueprint, jsonify
from .controllers.auth_controller import auth_bp
from .controllers.menu_controller import menu_bp

api_bp = Blueprint('api', __name__, url_prefix='/api/v1')

# Register Controllers
api_bp.register_blueprint(auth_bp)
api_bp.register_blueprint(menu_bp)

@api_bp.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "service": "S2O-Platform-Backend"}), 200

@api_bp.route('/', methods=['GET'])
def api_index():
    return jsonify({"message": "Welcome to S2O API v1"}), 200

