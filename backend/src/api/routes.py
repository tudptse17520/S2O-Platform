from flask import Blueprint, jsonify
from .controllers.auth_controller import auth_bp
from .controllers.menu_controller import menu_bp
from .controllers.tenant_controller import tenant_bp
from .controllers.branch_controller import branch_bp
from .controllers.order_controller import order_bp
from .controllers.table_controller import table_bp
from .controllers.reservation_controller import reservation_bp
from .controllers.review_controller import review_bp
from .controllers.invoice_controller import invoice_bp
from .controllers.promotion_controller import promotion_bp
from .controllers.payment_controller import payment_bp
from .controllers.customer_controller import customer_bp
from .controllers.staff_controller import staff_bp
from .controllers.user_controller import user_bp

api_bp = Blueprint('api', __name__, url_prefix='/api/v1')

# Register Controllers
api_bp.register_blueprint(auth_bp)
api_bp.register_blueprint(menu_bp)
api_bp.register_blueprint(tenant_bp)
api_bp.register_blueprint(branch_bp)
api_bp.register_blueprint(order_bp)
api_bp.register_blueprint(table_bp)
api_bp.register_blueprint(reservation_bp)
api_bp.register_blueprint(review_bp)
api_bp.register_blueprint(invoice_bp)
api_bp.register_blueprint(promotion_bp)
api_bp.register_blueprint(payment_bp)
api_bp.register_blueprint(customer_bp)
api_bp.register_blueprint(staff_bp)
api_bp.register_blueprint(user_bp)


@api_bp.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "service": "S2O-Platform-Backend"}), 200

@api_bp.route('/', methods=['GET'])
def api_index():
    return jsonify({"message": "Welcome to S2O API v1"}), 200

