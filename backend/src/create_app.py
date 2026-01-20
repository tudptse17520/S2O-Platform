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

    # Register API blueprints
    from api.controllers import (
        auth_controller,
        tenant_controller,
        branch_controller,
        menu_controller,
        order_controller,
        payment_controller,
        reservation_controller,
        table_controller,
        review_controller,
        chatbot_controller,
        recommendation_controller,
        report_controller
    )

    # Register all blueprints
    blueprints = [
        ("auth", auth_controller.auth_bp, "/api/v1/auth"),
        ("tenant", tenant_controller.tenant_bp, "/api/v1/tenants"),
        ("branch", branch_controller.branch_bp, "/api/v1/branches"),
        ("menu", menu_controller.menu_bp, "/api/v1/menus"),
        ("order", order_controller.order_bp, "/api/v1/orders"),
        ("payment", payment_controller.payment_bp, "/api/v1/payments"),
        ("reservation", reservation_controller.reservation_bp, "/api/v1/reservations"),
        ("table", table_controller.table_bp, "/api/v1/tables"),
        ("review", review_controller.review_bp, "/api/v1/reviews"),
        ("chatbot", chatbot_controller.chatbot_bp, "/api/v1/chatbot"),
        ("recommendation", recommendation_controller.recommendation_bp, "/api/v1/recommendations"),
        ("report", report_controller.report_bp, "/api/v1/reports"),
    ]

    for name, bp, url_prefix in blueprints:
        if bp:
            app.register_blueprint(bp, url_prefix=url_prefix)
            logger.info(f"Registered blueprint: {name} at {url_prefix}")

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
