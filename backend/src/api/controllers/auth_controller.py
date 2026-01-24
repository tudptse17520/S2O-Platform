from flask import Blueprint, request, jsonify
from pydantic import ValidationError
from ..schemas.auth_schemas import RegisterTenantRequest, LoginRequest
from src.services.auth_service import AuthService
from src.infrastructure.postgres import get_db
from src.infrastructure.repositories import SQLUserRepository, SQLTenantRepository

auth_bp = Blueprint('auth', __name__, url_prefix='/api/v1/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Register a new tenant and owner
    ---
    tags:
      - Auth
    parameters:
      - in: body
        name: body
        schema:
          id: RegisterTenantRequest
          required:
            - tenant_name
            - full_name
            - email
            - password
          properties:
            tenant_name:
              type: string
            full_name:
              type: string
            email:
              type: string
            password:
              type: string
    responses:
      201:
        description: Tenant registered successfully
      400:
        description: Validation error
    """
    data = request.get_json()
    db = next(get_db())
    try:
        # Validate
        req = RegisterTenantRequest(**data)
        
        # Dependency Injection
        user_repo = SQLUserRepository(db)
        tenant_repo = SQLTenantRepository(db)
        service = AuthService(user_repo, tenant_repo)
        
        # Execute Use Case
        result = service.register_tenant(req.model_dump())
        
        # Commit Transaction (Unit of Work)
        db.commit()
        
        return jsonify(result), 201
    except ValidationError as e:
        db.rollback()
        return jsonify({"error": "Validation Error", "details": e.errors()}), 400
    except ValueError as e:
        db.rollback()
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        db.rollback()
        import traceback
        traceback.print_exc()
        return jsonify({"error": "Internal Server Error"}), 500
    finally:
        db.close()

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Login and get JWT token
    ---
    tags:
      - Auth
    parameters:
      - in: body
        name: body
        schema:
          id: LoginRequest
          required:
            - email
            - password
          properties:
            email:
              type: string
            password:
              type: string
    responses:
      200:
        description: Login successful
      401:
        description: Invalid credentials
    """
    data = request.get_json()
    db = next(get_db())
    try:
        # Validate
        req = LoginRequest(**data)
        
        # Dependency Injection
        user_repo = SQLUserRepository(db)
        tenant_repo = SQLTenantRepository(db)
        service = AuthService(user_repo, tenant_repo)
        
        # Execute Use Case
        result = service.login(req.model_dump())
        
        return jsonify(result), 200
    except ValidationError as e:
        return jsonify({"error": "Validation Error", "details": e.errors()}), 400
    except ValueError as e:
        return jsonify({"error": str(e)}), 401
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": "Internal Server Error"}), 500
    finally:
        db.close()
