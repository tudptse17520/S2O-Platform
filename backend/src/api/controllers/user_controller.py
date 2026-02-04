from flask import Blueprint, request, jsonify, g
from pydantic import ValidationError
from ..schemas.user_schema import CreateUserRequest, UpdateUserRequest, ChangeRoleRequest
from ..middleware import auth_required
from ...services.user_service import UserService
from ...infrastructure.databases.postgres import get_db
from ...infrastructure.repositories.user_repository import UserRepository
import logging

logger = logging.getLogger(__name__)

user_bp = Blueprint("users", __name__, url_prefix="/users")


@user_bp.route("", methods=["GET"])
@auth_required(roles=['OWNER', 'SYS_ADMIN'])
def get_users():
    """
    Get all users for current tenant
    ---
    tags:
      - Users
    parameters:
      - in: header
        name: Authorization
        type: string
        required: true
    responses:
      200:
        description: List of users
    """
    db = next(get_db())
    try:
        user_repo = UserRepository(db)
        service = UserService(user_repo)
        
        users = service.get_users_by_tenant(g.tenant_id)
        return jsonify({"users": users}), 200
    except Exception as e:
        logger.error(f"Get users error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()


@user_bp.route("/all", methods=["GET"])
@auth_required(roles=['SYS_ADMIN'])
def get_all_users():
    """
    Get all users in system (SYS_ADMIN only)
    ---
    tags:
      - Users
    parameters:
      - in: header
        name: Authorization
        type: string
        required: true
    responses:
      200:
        description: List of all users
    """
    db = next(get_db())
    try:
        user_repo = UserRepository(db)
        service = UserService(user_repo)
        
        users = service.get_all_users()
        return jsonify({"users": users}), 200
    except Exception as e:
        logger.error(f"Get all users error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()


@user_bp.route("/me", methods=["GET"])
@auth_required()
def get_current_user():
    """
    Get current authenticated user profile
    ---
    tags:
      - Users
    parameters:
      - in: header
        name: Authorization
        type: string
        required: true
    responses:
      200:
        description: Current user profile
    """
    db = next(get_db())
    try:
        user_repo = UserRepository(db)
        service = UserService(user_repo)
        
        user = service.get_user(g.user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404
        return jsonify(user), 200
    except Exception as e:
        logger.error(f"Get current user error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()


@user_bp.route("/<user_id>", methods=["GET"])
@auth_required(roles=['OWNER', 'SYS_ADMIN'])
def get_user(user_id):
    """
    Get user by ID
    ---
    tags:
      - Users
    parameters:
      - in: header
        name: Authorization
        type: string
        required: true
      - in: path
        name: user_id
        type: string
        required: true
    responses:
      200:
        description: User details
      404:
        description: User not found
    """
    db = next(get_db())
    try:
        user_repo = UserRepository(db)
        service = UserService(user_repo)
        
        user = service.get_user(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404
        return jsonify(user), 200
    except Exception as e:
        logger.error(f"Get user error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()


@user_bp.route("", methods=["POST"])
@auth_required(roles=['OWNER', 'SYS_ADMIN'])
def create_user():
    """
    Create a new user
    ---
    tags:
      - Users
    parameters:
      - in: header
        name: Authorization
        type: string
        required: true
      - in: body
        name: body
        schema:
          id: CreateUserRequest
          required:
            - email
            - password
          properties:
            email:
              type: string
              format: email
            password:
              type: string
              minLength: 6
            full_name:
              type: string
            role:
              type: string
              enum: [SYS_ADMIN, OWNER, STAFF, CUSTOMER]
    responses:
      201:
        description: User created
    """
    data = request.get_json()
    db = next(get_db())
    try:
        req = CreateUserRequest(**data)
        
        user_repo = UserRepository(db)
        service = UserService(user_repo)
        
        result = service.create_user(req.model_dump(), g.tenant_id)
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
        logger.error(f"Create user error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()


@user_bp.route("/me", methods=["PUT"])
@auth_required()
def update_current_user():
    """
    Update current user profile
    ---
    tags:
      - Users
    parameters:
      - in: header
        name: Authorization
        type: string
        required: true
      - in: body
        name: body
        schema:
          id: UpdateUserRequest
          properties:
            full_name:
              type: string
    responses:
      200:
        description: Profile updated
    """
    data = request.get_json()
    db = next(get_db())
    try:
        req = UpdateUserRequest(**data)
        
        user_repo = UserRepository(db)
        service = UserService(user_repo)
        
        # Only allow updating full_name for self
        update_data = {"full_name": req.full_name} if req.full_name else {}
        result = service.update_user(g.user_id, update_data)
        db.commit()
        
        return jsonify(result), 200
    except ValidationError as e:
        db.rollback()
        return jsonify({"error": "Validation Error", "details": e.errors()}), 400
    except ValueError as e:
        db.rollback()
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        db.rollback()
        logger.error(f"Update current user error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()


@user_bp.route("/<user_id>", methods=["PUT"])
@auth_required(roles=['OWNER', 'SYS_ADMIN'])
def update_user(user_id):
    """
    Update user by ID
    ---
    tags:
      - Users
    parameters:
      - in: header
        name: Authorization
        type: string
        required: true
      - in: path
        name: user_id
        type: string
        required: true
      - in: body
        name: body
        schema:
          id: UpdateUserRequestAdmin
          properties:
            full_name:
              type: string
            role:
              type: string
              enum: [SYS_ADMIN, OWNER, STAFF, CUSTOMER]
    responses:
      200:
        description: User updated
    """
    data = request.get_json()
    db = next(get_db())
    try:
        req = UpdateUserRequest(**data)
        
        user_repo = UserRepository(db)
        service = UserService(user_repo)
        
        result = service.update_user(user_id, req.model_dump(exclude_unset=True))
        db.commit()
        
        return jsonify(result), 200
    except ValidationError as e:
        db.rollback()
        return jsonify({"error": "Validation Error", "details": e.errors()}), 400
    except ValueError as e:
        db.rollback()
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        db.rollback()
        logger.error(f"Update user error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()


@user_bp.route("/<user_id>/role", methods=["PUT"])
@auth_required(roles=['SYS_ADMIN'])
def change_user_role(user_id):
    """
    Change user role (SYS_ADMIN only)
    ---
    tags:
      - Users
    parameters:
      - in: header
        name: Authorization
        type: string
        required: true
      - in: path
        name: user_id
        type: string
        required: true
      - in: body
        name: body
        schema:
          id: ChangeRoleRequest
          required:
            - role
          properties:
            role:
              type: string
              enum: [SYS_ADMIN, OWNER, STAFF, CUSTOMER]
    responses:
      200:
        description: Role changed
    """
    data = request.get_json()
    db = next(get_db())
    try:
        req = ChangeRoleRequest(**data)
        
        user_repo = UserRepository(db)
        service = UserService(user_repo)
        
        result = service.change_user_role(user_id, req.role.value)
        db.commit()
        
        return jsonify(result), 200
    except ValidationError as e:
        db.rollback()
        return jsonify({"error": "Validation Error", "details": e.errors()}), 400
    except ValueError as e:
        db.rollback()
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        db.rollback()
        logger.error(f"Change user role error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()


@user_bp.route("/<user_id>", methods=["DELETE"])
@auth_required(roles=['OWNER', 'SYS_ADMIN'])
def delete_user(user_id):
    """
    Delete user
    ---
    tags:
      - Users
    parameters:
      - in: header
        name: Authorization
        type: string
        required: true
      - in: path
        name: user_id
        type: string
        required: true
    responses:
      200:
        description: User deleted
    """
    db = next(get_db())
    try:
        user_repo = UserRepository(db)
        service = UserService(user_repo)
        
        deleted = service.delete_user(user_id)
        db.commit()
        
        if deleted:
            return jsonify({"message": "User deleted"}), 200
        return jsonify({"error": "User not found"}), 404
    except Exception as e:
        db.rollback()
        logger.error(f"Delete user error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()
