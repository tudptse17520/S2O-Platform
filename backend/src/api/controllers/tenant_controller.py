from flask import Blueprint, request, jsonify, g
from pydantic import ValidationError
from ..schemas.tenant_schema import CreateTenantRequest, UpdateTenantRequest
from ..middleware import auth_required
from ...services.tenant_service import TenantService
from ...infrastructure.databases.postgres import get_db
from ...infrastructure.repositories import TenantRepository
import logging

logger = logging.getLogger(__name__)

tenant_bp = Blueprint("tenants", __name__, url_prefix="/tenants")


@tenant_bp.route("", methods=["GET"])
@auth_required(roles=['SYS_ADMIN'])
def get_tenants():
    """
    Get all tenants
    ---
    tags:
      - Tenants
    parameters:
      - in: header
        name: Authorization
        type: string
        required: true
        description: Bearer <token>
    responses:
      200:
        description: List of all tenants
      401:
        description: Unauthorized
      403:
        description: Forbidden
    """
    db = next(get_db())
    try:
        tenant_repo = TenantRepository(db)
        service = TenantService(tenant_repo)
        
        tenants = service.get_all_tenants()
        return jsonify({"tenants": tenants}), 200
    except Exception as e:
        logger.error(f"Get tenants error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()


@tenant_bp.route("/<tenant_id>", methods=["GET"])
@auth_required(roles=['SYS_ADMIN', 'OWNER'])
def get_tenant(tenant_id):
    """
    Get tenant by ID
    ---
    tags:
      - Tenants
    parameters:
      - in: header
        name: Authorization
        type: string
        required: true
      - in: path
        name: tenant_id
        type: string
        required: true
    responses:
      200:
        description: Tenant details
      404:
        description: Tenant not found
    """
    db = next(get_db())
    try:
        tenant_repo = TenantRepository(db)
        service = TenantService(tenant_repo)
        
        tenant = service.get_tenant(tenant_id)
        if not tenant:
            return jsonify({"error": "Tenant not found"}), 404
        return jsonify(tenant), 200
    except Exception as e:
        logger.error(f"Get tenant error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()


@tenant_bp.route("", methods=["POST"])
@auth_required(roles=['SYS_ADMIN'])
def create_tenant():
    """
    Create new tenant
    ---
    tags:
      - Tenants
    parameters:
      - in: header
        name: Authorization
        type: string
        required: true
      - in: body
        name: body
        schema:
          id: CreateTenantRequest
          required:
            - name
          properties:
            name:
              type: string
            subscription_plan:
              type: string
            is_active:
              type: boolean
    responses:
      201:
        description: Tenant created successfully
      400:
        description: Validation error
    """
    data = request.get_json()
    db = next(get_db())
    try:
        req = CreateTenantRequest(**data)
        
        tenant_repo = TenantRepository(db)
        service = TenantService(tenant_repo)
        
        result = service.create_tenant(req.model_dump())
        db.commit()
        
        return jsonify(result), 201
    except ValidationError as e:
        db.rollback()
        return jsonify({"error": "Validation Error", "details": e.errors()}), 400
    except Exception as e:
        db.rollback()
        logger.error(f"Create tenant error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()


@tenant_bp.route("/<tenant_id>", methods=["PUT"])
@auth_required(roles=['SYS_ADMIN'])
def update_tenant(tenant_id):
    """
    Update tenant
    ---
    tags:
      - Tenants
    parameters:
      - in: header
        name: Authorization
        type: string
        required: true
      - in: path
        name: tenant_id
        type: string
        required: true
      - in: body
        name: body
        schema:
          id: UpdateTenantRequest
          properties:
            name:
              type: string
            subscription_plan:
              type: string
            is_active:
              type: boolean
    responses:
      200:
        description: Tenant updated successfully
      404:
        description: Tenant not found
    """
    data = request.get_json()
    db = next(get_db())
    try:
        req = UpdateTenantRequest(**data)
        
        tenant_repo = TenantRepository(db)
        service = TenantService(tenant_repo)
        
        result = service.update_tenant(tenant_id, req.model_dump(exclude_unset=True))
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
        logger.error(f"Update tenant error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()


@tenant_bp.route("/<tenant_id>", methods=["DELETE"])
@auth_required(roles=['SYS_ADMIN'])
def delete_tenant(tenant_id):
    """
    Deactivate tenant (soft delete)
    ---
    tags:
      - Tenants
    parameters:
      - in: header
        name: Authorization
        type: string
        required: true
      - in: path
        name: tenant_id
        type: string
        required: true
    responses:
      200:
        description: Tenant deactivated
      404:
        description: Tenant not found
    """
    db = next(get_db())
    try:
        tenant_repo = TenantRepository(db)
        service = TenantService(tenant_repo)
        
        result = service.deactivate_tenant(tenant_id)
        db.commit()
        
        return jsonify({"message": "Tenant deactivated", "tenant": result}), 200
    except ValueError as e:
        db.rollback()
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        db.rollback()
        logger.error(f"Delete tenant error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()
