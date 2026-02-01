from flask import Blueprint, request, jsonify, g
from pydantic import ValidationError
from ..schemas.staff_profile_schema import CreateStaffProfileRequest, UpdateStaffProfileRequest
from ..middleware import auth_required
from ...services.staff_profile_service import StaffProfileService
from ...infrastructure.databases.postgres import get_db
from ...infrastructure.repositories.staff_profile_repository import StaffProfileRepository
import logging

logger = logging.getLogger(__name__)

staff_bp = Blueprint("staff", __name__, url_prefix="/staff")


@staff_bp.route("", methods=["GET"])
@auth_required(roles=['OWNER', 'SYS_ADMIN'])
def get_staff():
    """
    Get all staff for current tenant
    ---
    tags:
      - Staff
    parameters:
      - in: header
        name: Authorization
        type: string
        required: true
      - in: query
        name: position
        type: string
        description: Filter by position
    responses:
      200:
        description: List of staff
    """
    db = next(get_db())
    try:
        position = request.args.get('position')
        
        staff_repo = StaffProfileRepository(db)
        service = StaffProfileService(staff_repo)
        
        if position:
            staff = service.get_staff_by_position(g.tenant_id, position)
        else:
            staff = service.get_staff_by_tenant(g.tenant_id)
        
        return jsonify({"staff": staff}), 200
    except Exception as e:
        logger.error(f"Get staff error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()


@staff_bp.route("/me", methods=["GET"])
@auth_required(roles=['OWNER', 'STAFF', 'SYS_ADMIN'])
def get_my_profile():
    """
    Get current user's staff profile
    ---
    tags:
      - Staff
    parameters:
      - in: header
        name: Authorization
        type: string
        required: true
    responses:
      200:
        description: Staff profile
      404:
        description: Profile not found
    """
    db = next(get_db())
    try:
        staff_repo = StaffProfileRepository(db)
        service = StaffProfileService(staff_repo)
        
        profile = service.get_staff_profile(g.user_id)
        if not profile:
            return jsonify({"error": "Staff profile not found"}), 404
        return jsonify(profile), 200
    except Exception as e:
        logger.error(f"Get my staff profile error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()


@staff_bp.route("/<user_id>", methods=["GET"])
@auth_required(roles=['OWNER', 'SYS_ADMIN'])
def get_staff_profile(user_id):
    """
    Get staff profile by user ID
    ---
    tags:
      - Staff
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
        description: Staff profile
      404:
        description: Staff not found
    """
    db = next(get_db())
    try:
        staff_repo = StaffProfileRepository(db)
        service = StaffProfileService(staff_repo)
        
        profile = service.get_staff_profile(user_id)
        if not profile:
            return jsonify({"error": "Staff profile not found"}), 404
        return jsonify(profile), 200
    except Exception as e:
        logger.error(f"Get staff profile error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()


@staff_bp.route("/branch/<branch_id>", methods=["GET"])
@auth_required(roles=['OWNER', 'STAFF', 'SYS_ADMIN'])
def get_staff_by_branch(branch_id):
    """
    Get staff by branch
    ---
    tags:
      - Staff
    parameters:
      - in: header
        name: Authorization
        type: string
        required: true
      - in: path
        name: branch_id
        type: string
        required: true
    responses:
      200:
        description: List of staff for branch
    """
    db = next(get_db())
    try:
        staff_repo = StaffProfileRepository(db)
        service = StaffProfileService(staff_repo)
        
        staff = service.get_staff_by_branch(branch_id)
        return jsonify({"staff": staff}), 200
    except Exception as e:
        logger.error(f"Get staff by branch error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()


@staff_bp.route("", methods=["POST"])
@auth_required(roles=['OWNER', 'SYS_ADMIN'])
def create_staff_profile():
    """
    Create staff profile
    ---
    tags:
      - Staff
    parameters:
      - in: header
        name: Authorization
        type: string
        required: true
      - in: query
        name: user_id
        type: string
        required: true
        description: User ID to create staff profile for
      - in: body
        name: body
        schema:
          id: CreateStaffProfileRequest
          properties:
            branch_id:
              type: string
            position:
              type: string
    responses:
      201:
        description: Staff profile created
    """
    data = request.get_json() or {}
    user_id = request.args.get('user_id')
    
    if not user_id:
        return jsonify({"error": "user_id query parameter required"}), 400
    
    db = next(get_db())
    try:
        req = CreateStaffProfileRequest(**data)
        
        staff_repo = StaffProfileRepository(db)
        service = StaffProfileService(staff_repo)
        
        result = service.create_staff_profile(user_id, g.tenant_id, req.model_dump())
        db.commit()
        
        return jsonify(result), 201
    except ValidationError as e:
        db.rollback()
        return jsonify({"error": "Validation Error", "details": e.errors()}), 400
    except Exception as e:
        db.rollback()
        logger.error(f"Create staff profile error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()


@staff_bp.route("/<user_id>", methods=["PUT"])
@auth_required(roles=['OWNER', 'SYS_ADMIN'])
def update_staff_profile(user_id):
    """
    Update staff profile
    ---
    tags:
      - Staff
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
          id: UpdateStaffProfileRequest
          properties:
            branch_id:
              type: string
            position:
              type: string
    responses:
      200:
        description: Staff profile updated
    """
    data = request.get_json()
    db = next(get_db())
    try:
        req = UpdateStaffProfileRequest(**data)
        
        staff_repo = StaffProfileRepository(db)
        service = StaffProfileService(staff_repo)
        
        result = service.update_staff_profile(user_id, req.model_dump(exclude_unset=True))
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
        logger.error(f"Update staff profile error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()


@staff_bp.route("/<user_id>", methods=["DELETE"])
@auth_required(roles=['OWNER', 'SYS_ADMIN'])
def delete_staff_profile(user_id):
    """
    Delete staff profile
    ---
    tags:
      - Staff
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
        description: Staff profile deleted
    """
    db = next(get_db())
    try:
        staff_repo = StaffProfileRepository(db)
        service = StaffProfileService(staff_repo)
        
        deleted = service.delete_staff_profile(user_id)
        db.commit()
        
        if deleted:
            return jsonify({"message": "Staff profile deleted"}), 200
        return jsonify({"error": "Staff profile not found"}), 404
    except Exception as e:
        db.rollback()
        logger.error(f"Delete staff profile error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()
