from flask import Blueprint, request, jsonify, g
from pydantic import ValidationError
from ..schemas.branch_schema import CreateBranchRequest, UpdateBranchRequest
from ..middleware import auth_required
from ...services.branch_service import BranchService
from ...infrastructure.databases.postgres import get_db
from ...infrastructure.repositories import BranchRepository
import logging

logger = logging.getLogger(__name__)

branch_bp = Blueprint("branches", __name__, url_prefix="/branches")


@branch_bp.route("", methods=["GET"])
@auth_required()
def get_branches():
    """
    Get all branches for current tenant
    ---
    tags:
      - Branches
    parameters:
      - in: header
        name: Authorization
        type: string
        required: true
        description: Bearer <token>
    responses:
      200:
        description: List of branches
      401:
        description: Unauthorized
    """
    db = next(get_db())
    try:
        branch_repo = BranchRepository(db)
        service = BranchService(branch_repo)
        
        branches = service.get_branches_by_tenant(g.tenant_id)
        return jsonify({"branches": branches}), 200
    except Exception as e:
        logger.error(f"Get branches error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()


@branch_bp.route("/<branch_id>", methods=["GET"])
@auth_required()
def get_branch(branch_id):
    """
    Get branch by ID
    ---
    tags:
      - Branches
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
        description: Branch details
      404:
        description: Branch not found
    """
    db = next(get_db())
    try:
        branch_repo = BranchRepository(db)
        service = BranchService(branch_repo)
        
        branch = service.get_branch(branch_id)
        if not branch:
            return jsonify({"error": "Branch not found"}), 404
        return jsonify(branch), 200
    except Exception as e:
        logger.error(f"Get branch error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()


@branch_bp.route("", methods=["POST"])
@auth_required(roles=['OWNER', 'SYS_ADMIN'])
def create_branch():
    """
    Create new branch
    ---
    tags:
      - Branches
    parameters:
      - in: header
        name: Authorization
        type: string
        required: true
      - in: body
        name: body
        schema:
          id: CreateBranchRequest
          required:
            - name
          properties:
            name:
              type: string
            address:
              type: string
            is_active:
              type: boolean
    responses:
      201:
        description: Branch created successfully
      400:
        description: Validation error
    """
    data = request.get_json()
    db = next(get_db())
    try:
        req = CreateBranchRequest(**data)
        
        branch_repo = BranchRepository(db)
        service = BranchService(branch_repo)
        
        result = service.create_branch(g.tenant_id, req.model_dump())
        db.commit()
        
        return jsonify(result), 201
    except ValidationError as e:
        db.rollback()
        return jsonify({"error": "Validation Error", "details": e.errors()}), 400
    except Exception as e:
        db.rollback()
        logger.error(f"Create branch error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()


@branch_bp.route("/<branch_id>", methods=["PUT"])
@auth_required(roles=['OWNER', 'SYS_ADMIN'])
def update_branch(branch_id):
    """
    Update branch
    ---
    tags:
      - Branches
    parameters:
      - in: header
        name: Authorization
        type: string
        required: true
      - in: path
        name: branch_id
        type: string
        required: true
      - in: body
        name: body
        schema:
          id: UpdateBranchRequest
          properties:
            name:
              type: string
            address:
              type: string
            is_active:
              type: boolean
    responses:
      200:
        description: Branch updated successfully
      404:
        description: Branch not found
    """
    data = request.get_json()
    db = next(get_db())
    try:
        req = UpdateBranchRequest(**data)
        
        branch_repo = BranchRepository(db)
        service = BranchService(branch_repo)
        
        result = service.update_branch(branch_id, req.model_dump(exclude_unset=True))
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
        logger.error(f"Update branch error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()


@branch_bp.route("/<branch_id>", methods=["DELETE"])
@auth_required(roles=['OWNER', 'SYS_ADMIN'])
def delete_branch(branch_id):
    """
    Delete branch
    ---
    tags:
      - Branches
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
        description: Branch deleted
      404:
        description: Branch not found
    """
    db = next(get_db())
    try:
        branch_repo = BranchRepository(db)
        service = BranchService(branch_repo)
        
        deleted = service.delete_branch(branch_id)
        db.commit()
        
        if deleted:
            return jsonify({"message": "Branch deleted"}), 200
        return jsonify({"error": "Branch not found"}), 404
    except Exception as e:
        db.rollback()
        logger.error(f"Delete branch error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()
