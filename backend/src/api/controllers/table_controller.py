from flask import Blueprint, request, jsonify, g
from pydantic import ValidationError
from ..schemas.table_schema import CreateTableRequest, UpdateTableRequest, UpdateTableStatusRequest
from ..middleware import auth_required
from ...services.table_service import TableService
from ...infrastructure.databases.postgres import get_db
from ...infrastructure.repositories import TableRepository
import logging

logger = logging.getLogger(__name__)

table_bp = Blueprint("tables", __name__, url_prefix="/tables")


@table_bp.route("", methods=["GET"])
@auth_required()
def get_tables():
    """
    Get all tables for current tenant
    ---
    tags:
      - Tables
    parameters:
      - in: header
        name: Authorization
        type: string
        required: true
      - in: query
        name: branch_id
        type: string
        description: Filter by branch
      - in: query
        name: status
        type: string
        description: Filter by status (AVAILABLE, OCCUPIED)
    responses:
      200:
        description: List of tables
    """
    db = next(get_db())
    try:
        branch_id = request.args.get('branch_id')
        status = request.args.get('status')
        
        table_repo = TableRepository(db)
        service = TableService(table_repo)
        
        if branch_id:
            tables = service.get_tables_by_branch(branch_id)
        elif status and status.upper() == 'AVAILABLE':
            tables = service.get_available_tables(g.tenant_id)
        else:
            tables = service.get_tables_by_tenant(g.tenant_id)
        
        return jsonify({"tables": tables}), 200
    except Exception as e:
        logger.error(f"Get tables error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()


@table_bp.route("/<table_id>", methods=["GET"])
@auth_required()
def get_table(table_id):
    """
    Get table by ID
    ---
    tags:
      - Tables
    parameters:
      - in: header
        name: Authorization
        type: string
        required: true
      - in: path
        name: table_id
        type: string
        required: true
    responses:
      200:
        description: Table details
      404:
        description: Table not found
    """
    db = next(get_db())
    try:
        table_repo = TableRepository(db)
        service = TableService(table_repo)
        
        table = service.get_table(table_id)
        if not table:
            return jsonify({"error": "Table not found"}), 404
        return jsonify(table), 200
    except Exception as e:
        logger.error(f"Get table error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()


@table_bp.route("", methods=["POST"])
@auth_required(roles=['OWNER', 'STAFF', 'SYS_ADMIN'])
def create_table():
    """
    Create new table
    ---
    tags:
      - Tables
    parameters:
      - in: header
        name: Authorization
        type: string
        required: true
      - in: body
        name: body
        schema:
          id: CreateTableRequest
          required:
            - branch_id
            - name
          properties:
            branch_id:
              type: string
            name:
              type: string
    responses:
      201:
        description: Table created
    """
    data = request.get_json()
    db = next(get_db())
    try:
        req = CreateTableRequest(**data)
        
        table_repo = TableRepository(db)
        service = TableService(table_repo)
        
        result = service.create_table(g.tenant_id, req.branch_id, req.model_dump())
        db.commit()
        
        return jsonify(result), 201
    except ValidationError as e:
        db.rollback()
        return jsonify({"error": "Validation Error", "details": e.errors()}), 400
    except Exception as e:
        db.rollback()
        logger.error(f"Create table error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()


@table_bp.route("/<table_id>", methods=["PUT"])
@auth_required(roles=['OWNER', 'STAFF', 'SYS_ADMIN'])
def update_table(table_id):
    """
    Update table
    ---
    tags:
      - Tables
    parameters:
      - in: header
        name: Authorization
        type: string
        required: true
      - in: path
        name: table_id
        type: string
        required: true
      - in: body
        name: body
        schema:
          id: UpdateTableRequest
          properties:
            name:
              type: string
    responses:
      200:
        description: Table updated
    """
    data = request.get_json()
    db = next(get_db())
    try:
        req = UpdateTableRequest(**data)
        
        table_repo = TableRepository(db)
        service = TableService(table_repo)
        
        result = service.update_table(table_id, req.model_dump(exclude_unset=True))
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
        logger.error(f"Update table error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()


@table_bp.route("/<table_id>/status", methods=["PUT"])
@auth_required(roles=['OWNER', 'STAFF', 'SYS_ADMIN'])
def update_table_status(table_id):
    """
    Update table status
    ---
    tags:
      - Tables
    parameters:
      - in: header
        name: Authorization
        type: string
        required: true
      - in: path
        name: table_id
        type: string
        required: true
      - in: body
        name: body
        schema:
          id: UpdateTableStatusRequest
          required:
            - status
          properties:
            status:
              type: string
              description: AVAILABLE or OCCUPIED
    responses:
      200:
        description: Table status updated
    """
    data = request.get_json()
    db = next(get_db())
    try:
        req = UpdateTableStatusRequest(**data)
        
        table_repo = TableRepository(db)
        service = TableService(table_repo)
        
        result = service.update_table_status(table_id, req.status)
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
        logger.error(f"Update table status error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()


@table_bp.route("/<table_id>/qr", methods=["GET"])
@auth_required()
def get_table_qr(table_id):
    """
    Get QR code URL for table
    ---
    tags:
      - Tables
    parameters:
      - in: header
        name: Authorization
        type: string
        required: true
      - in: path
        name: table_id
        type: string
        required: true
    responses:
      200:
        description: QR code URL
    """
    db = next(get_db())
    try:
        table_repo = TableRepository(db)
        service = TableService(table_repo)
        
        base_url = request.host_url.rstrip('/')
        qr_url = service.generate_qr_code(table_id, base_url)
        
        return jsonify({"qr_code_url": qr_url}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        logger.error(f"Get table QR error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()


@table_bp.route("/<table_id>", methods=["DELETE"])
@auth_required(roles=['OWNER', 'SYS_ADMIN'])
def delete_table(table_id):
    """
    Delete table
    ---
    tags:
      - Tables
    parameters:
      - in: header
        name: Authorization
        type: string
        required: true
      - in: path
        name: table_id
        type: string
        required: true
    responses:
      200:
        description: Table deleted
    """
    db = next(get_db())
    try:
        table_repo = TableRepository(db)
        service = TableService(table_repo)
        
        deleted = service.delete_table(table_id)
        db.commit()
        
        if deleted:
            return jsonify({"message": "Table deleted"}), 200
        return jsonify({"error": "Table not found"}), 404
    except Exception as e:
        db.rollback()
        logger.error(f"Delete table error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()
