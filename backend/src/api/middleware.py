from functools import wraps
from flask import request, jsonify, g
import jwt
from config import Config

def auth_required(roles=None):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            token = None
            
            if 'Authorization' in request.headers:
                auth_header = request.headers['Authorization']
                if auth_header.startswith('Bearer '):
                    token = auth_header.split(" ")[1]
            
            if not token:
                return jsonify({"error": "Authorization token is missing", "code": 401}), 401
            
            try:
                payload = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
                g.user_id = payload['sub']
                g.tenant_id = payload['tenant_id']
                g.role = payload['role']
                
                # Check Role
                if roles and payload['role'] not in roles:
                    return jsonify({"error": "Forbidden: Insufficient permissions", "code": 403}), 403
                    
            except jwt.ExpiredSignatureError:
                return jsonify({"error": "Token has expired", "code": 401}), 401
            except jwt.InvalidTokenError:
                return jsonify({"error": "Invalid token", "code": 401}), 401
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator
