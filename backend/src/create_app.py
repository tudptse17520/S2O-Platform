import os
from flask import Flask, jsonify
from .config import config
from .infrastructure.databases.postgres import db_session
from .api.routes import api_bp
from .cors import setup_cors
from .error_handler import register_error_handlers
from .app_logging import setup_logging

def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'default')

    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Initialize extensions
    setup_cors(app)
    setup_logging(app)
    register_error_handlers(app)

    # Swagger Configuration
    from flasgger import Swagger
    import json
    
    swagger_config_path = os.path.join(os.path.dirname(__file__), 'swagger_config.json')
    try:
        with open(swagger_config_path, 'r') as f:
            template = json.load(f)
    except FileNotFoundError:
        template = {
            "swagger": "2.0",
            "info": {
                "title": "S2O Platform API",
                "version": "1.0.0",
                "description": "API Documentation"
            }
        }

    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": "apispec",
                "route": "/apispec.json",
                "rule_filter": lambda rule: True,  # all in
                "model_filter": lambda tag: True,  # all in
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/docs"
    }

    Swagger(app, template=template, config=swagger_config)

    # Register Blueprints
    app.register_blueprint(api_bp)
    
    # Root Route
    @app.route('/')
    def index():
        return jsonify({
            "name": "S2O SaaS Platform API",
            "version": "1.0.0",
            "docs": "/docs",
            "spec": "/apispec.json"
        })

    # Teardown database session
    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()

    return app
