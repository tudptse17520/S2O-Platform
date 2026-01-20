from flask import jsonify
from datetime import datetime


def success_response(data=None, code=200, message="Success"):
    """
    Return a standardized success response
    
    Args:
        data: Response data
        code: HTTP status code
        message: Success message
    """
    response = {
        "status": "success",
        "code": code,
        "message": message,
        "data": data,
        "timestamp": datetime.utcnow().isoformat()
    }
    return jsonify(response), code


def error_response(message, code=400, error_code=None, details=None):
    """
    Return a standardized error response
    
    Args:
        message: Error message
        code: HTTP status code
        error_code: Custom error code
        details: Additional error details
    """
    response = {
        "status": "error",
        "code": code,
        "message": message,
        "error_code": error_code,
        "details": details,
        "timestamp": datetime.utcnow().isoformat()
    }
    return jsonify(response), code


def paginated_response(items, total, page, per_page, code=200):
    """
    Return a paginated response
    
    Args:
        items: List of items
        total: Total number of items
        page: Current page number
        per_page: Items per page
        code: HTTP status code
    """
    response = {
        "status": "success",
        "code": code,
        "data": items,
        "pagination": {
            "total": total,
            "page": page,
            "per_page": per_page,
            "total_pages": (total + per_page - 1) // per_page
        },
        "timestamp": datetime.utcnow().isoformat()
    }
    return jsonify(response), code
