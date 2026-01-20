import logging
from functools import wraps
from flask import request, g
import uuid

logger = logging.getLogger(__name__)


def add_request_id():
    """Add request ID to each request for tracking"""
    g.request_id = str(uuid.uuid4())
    logger.info(f"Request ID: {g.request_id} - {request.method} {request.path}")


def register_middleware(app):
    """Register all middleware"""
    app.before_request(add_request_id)
