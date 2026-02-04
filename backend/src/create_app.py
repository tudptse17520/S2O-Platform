import os
from flask import Flask, jsonify
from .config import config
from .infrastructure.databases.postgres import db_session
from .api.routes import api_bp
from .cors import setup_cors
from .error_handler import register_error_handlers
from .app_logging import setup_logging

# Global service instances
_cache_service = None
_realtime_service = None


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'default')

    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Initialize core extensions
    setup_cors(app)
    setup_logging(app)
    register_error_handlers(app)

    # Initialize infrastructure services
    _init_services(app)

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
                "rule_filter": lambda rule: True,
                "model_filter": lambda tag: True,
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
            "spec": "/apispec.json",
            "services": {
                "cache": _cache_service.is_available if _cache_service else False,
                "realtime": _realtime_service.is_available if _realtime_service else False
            }
        })

    # Teardown database session
    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()

    return app


def _init_services(app):
    """Initialize infrastructure services"""
    global _cache_service, _realtime_service
    
    # Initialize Cache Service
    try:
        from .infrastructure.services.cache_service import init_cache_service
        _cache_service = init_cache_service(app)
    except Exception as e:
        app.logger.warning(f"Cache service initialization failed: {e}")
    
    # Initialize Realtime Service (only if explicitly enabled)
    if os.getenv('ENABLE_REALTIME', 'false').lower() == 'true':
        try:
            from .infrastructure.services.realtime_service import init_realtime_service
            _realtime_service = init_realtime_service(app)
        except Exception as e:
            app.logger.warning(f"Realtime service initialization failed: {e}")


def create_app_with_realtime(config_name=None):
    """Create app with realtime service enabled"""
    os.environ['ENABLE_REALTIME'] = 'true'
    app = create_app(config_name)
    return app, _realtime_service.socketio if _realtime_service else None


def get_cache_service():
    """Get cache service instance"""
    return _cache_service


def get_realtime_service():
    """Get realtime service instance"""
    return _realtime_service
