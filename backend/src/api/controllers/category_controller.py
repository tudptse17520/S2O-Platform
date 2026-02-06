from flask import Blueprint, request, jsonify, g
from pydantic import ValidationError
from ..schemas.category_schema import CreateCategoryRequest, UpdateCategoryRequest
from ..middleware import auth_required
from ...services.category_service import CategoryService
from ...infrastructure.databases.postgres import get_db
from ...infrastructure.repositories.category_repository import CategoryRepository
import logging

logger = logging.getLogger(__name__)

category_bp = Blueprint("categories", __name__, url_prefix="/categories")


@category_bp.route("", methods=["GET"])
@auth_required()
def get_categories():
    """
    Get all categories for current tenant
    ---
    tags:
      - Categories
    parameters:
      - in: header
        name: Authorization
        type: string
        required: true
        description: Bearer token
    responses:
      200:
        description: List of categories
        schema:
          type: object
          properties:
            categories:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: string
                  name:
                    type: string
                  display_order:
                    type: integer
    """
    db = next(get_db())
    try:
        category_repo = CategoryRepository(db)
        service = CategoryService(category_repo)
        
        categories = service.get_categories_by_tenant(g.tenant_id)
        return jsonify({"categories": categories}), 200
    except Exception as e:
        logger.error(f"Get categories error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()


@category_bp.route("/<category_id>", methods=["GET"])
@auth_required()
def get_category(category_id):
    """
    Get category by ID
    ---
    tags:
      - Categories
    parameters:
      - in: header
        name: Authorization
        type: string
        required: true
      - in: path
        name: category_id
        type: string
        required: true
    responses:
      200:
        description: Category details
      404:
        description: Category not found
    """
    db = next(get_db())
    try:
        category_repo = CategoryRepository(db)
        service = CategoryService(category_repo)
        
        category = service.get_category(category_id)
        if not category:
            return jsonify({"error": "Category not found"}), 404
        return jsonify(category), 200
    except Exception as e:
        logger.error(f"Get category error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()


@category_bp.route("", methods=["POST"])
@auth_required(roles=['OWNER', 'SYS_ADMIN'])
def create_category():
    """
    Create new category
    ---
    tags:
      - Categories
    parameters:
      - in: header
        name: Authorization
        type: string
        required: true
      - in: body
        name: body
        schema:
          id: CreateCategoryRequest
          required:
            - name
          properties:
            name:
              type: string
              description: Category name
            display_order:
              type: integer
              description: Display order (default 0)
    responses:
      201:
        description: Category created
      400:
        description: Validation error
    """
    data = request.get_json()
    db = next(get_db())
    try:
        req = CreateCategoryRequest(**data)
        
        category_repo = CategoryRepository(db)
        service = CategoryService(category_repo)
        
        result = service.create_category(g.tenant_id, req.model_dump())
        db.commit()
        
        return jsonify(result), 201
    except ValidationError as e:
        db.rollback()
        return jsonify({"error": "Validation Error", "details": e.errors()}), 400
    except Exception as e:
        db.rollback()
        logger.error(f"Create category error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()


@category_bp.route("/<category_id>", methods=["PUT"])
@auth_required(roles=['OWNER', 'SYS_ADMIN'])
def update_category(category_id):
    """
    Update category
    ---
    tags:
      - Categories
    parameters:
      - in: header
        name: Authorization
        type: string
        required: true
      - in: path
        name: category_id
        type: string
        required: true
      - in: body
        name: body
        schema:
          id: UpdateCategoryRequest
          properties:
            name:
              type: string
            display_order:
              type: integer
    responses:
      200:
        description: Category updated
      404:
        description: Category not found
    """
    data = request.get_json()
    db = next(get_db())
    try:
        req = UpdateCategoryRequest(**data)
        
        category_repo = CategoryRepository(db)
        service = CategoryService(category_repo)
        
        result = service.update_category(category_id, req.model_dump(exclude_unset=True))
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
        logger.error(f"Update category error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()


@category_bp.route("/<category_id>", methods=["DELETE"])
@auth_required(roles=['OWNER', 'SYS_ADMIN'])
def delete_category(category_id):
    """
    Delete category
    ---
    tags:
      - Categories
    parameters:
      - in: header
        name: Authorization
        type: string
        required: true
      - in: path
        name: category_id
        type: string
        required: true
    responses:
      200:
        description: Category deleted
      404:
        description: Category not found
    """
    db = next(get_db())
    try:
        category_repo = CategoryRepository(db)
        service = CategoryService(category_repo)
        
        deleted = service.delete_category(category_id)
        db.commit()
        
        if deleted:
            return jsonify({"message": "Category deleted"}), 200
        return jsonify({"error": "Category not found"}), 404
    except Exception as e:
        db.rollback()
        logger.error(f"Delete category error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()


@category_bp.route("/reorder", methods=["POST"])
@auth_required(roles=['OWNER', 'SYS_ADMIN'])
def reorder_categories():
    """
    Reorder categories
    ---
    tags:
      - Categories
    parameters:
      - in: header
        name: Authorization
        type: string
        required: true
      - in: body
        name: body
        schema:
          type: object
          required:
            - order
          properties:
            order:
              type: array
              items:
                type: string
              description: Array of category IDs in desired order
    responses:
      200:
        description: Categories reordered
    """
    data = request.get_json()
    db = next(get_db())
    try:
        order = data.get('order', [])
        if not isinstance(order, list):
            return jsonify({"error": "order must be an array of category IDs"}), 400
        
        category_repo = CategoryRepository(db)
        service = CategoryService(category_repo)
        
        result = service.reorder_categories(g.tenant_id, order)
        db.commit()
        
        return jsonify({"categories": result}), 200
    except Exception as e:
        db.rollback()
        logger.error(f"Reorder categories error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()
