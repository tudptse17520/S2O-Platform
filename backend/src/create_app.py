from flask import Flask, jsonify
from flasgger import Swagger
from flask_cors import CORS
from infrastructure.databases import init_db
from config import get_config
from app_logging import setup_logging
import json
import os
import logging

logger = logging.getLogger(__name__)


def create_app():
    """
    Application factory for S2O-Platform Backend
    """
    app = Flask(__name__)

    # Load config
    app.config.from_object(get_config())

    # Setup logging
    setup_logging()

    # Setup CORS
    CORS(app)

    # Initialize Database
    try:
        init_db(app)
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        raise

    # Register middleware
    from api.middleware import register_middleware
    register_middleware(app)

    # Swagger config
    swagger_path = os.path.join(
        os.path.dirname(__file__),
        "swagger_config.json"
    )

    with open(swagger_path, "r", encoding="utf-8") as f:
        swagger_template = json.load(f)

    Swagger(app, template=swagger_template)

    # Health check endpoint
    @app.route("/health", methods=["GET"])
    def health_check():
        return jsonify({
            "status": "OK",
            "service": "S2O Backend",
            "version": "1.0.0"
        })

    # Register API blueprints dynamically and skip any that fail to import
    import importlib

    controller_configs = [
        ("auth_controller", "/api/v1/auth"),
        ("tenant_controller", "/api/v1/tenants"),
        ("branch_controller", "/api/v1/branches"),
        ("menu_controller", "/api/v1/menus"),
        ("order_controller", "/api/v1/orders"),
        ("payment_controller", "/api/v1/payments"),
        ("reservation_controller", "/api/v1/reservations"),
        ("table_controller", "/api/v1/tables"),
        ("review_controller", "/api/v1/reviews"),
        ("chatbot_controller", "/api/v1/chatbot"),
        ("recommendation_controller", "/api/v1/recommendations"),
        ("report_controller", "/api/v1/reports"),
        ("order_item_controller", "/api/v1/order-items"),
    ]

    for module_name, url_prefix in controller_configs:
        try:
            mod = importlib.import_module(f"api.controllers.{module_name}")
            prefix = module_name.replace("_controller", "")
            bp = getattr(mod, f"{prefix}_bp", None)
            if bp:
                app.register_blueprint(bp, url_prefix=url_prefix)
                logger.info(f"Registered blueprint: {prefix} at {url_prefix}")
            else:
                logger.warning(f"Controller {module_name} has no blueprint attribute; skipped")
        except Exception as e:
            logger.warning(f"Skipping controller {module_name} due to import error: {e}")

    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "status": "error",
            "code": 404,
            "message": "Endpoint not found"
        }), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            "status": "error",
            "code": 500,
            "message": "Internal server error"
        }), 500

    return app
