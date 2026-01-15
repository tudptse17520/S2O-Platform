from flask import Flask, jsonify
from flasgger import Swagger
from config import get_config
from app_logging import setup_logging
import json
import os


def create_app():
    app = Flask(__name__)

    # Load config
    app.config.from_object(get_config())

    # Setup logging
    setup_logging()

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
            "service": "S2O Backend"
        })

    return app
