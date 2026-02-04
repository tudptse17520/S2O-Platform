from flask import Blueprint, request, jsonify, g
from pydantic import ValidationError
from ..schemas.menu_schema import CreateCategoryRequest, CreateProductRequest, CategoryResponse, ProductResponse
from ...services.menu_service import MenuService
from ...infrastructure.databases.postgres import get_db
from ...infrastructure.repositories import CategoryRepository, ProductRepository
from ..middleware import auth_required
from ..controllers.utils import standardize_response

menu_bp = Blueprint('menu', __name__, url_prefix='/menu')

@menu_bp.route('/categories', methods=['POST'])
@auth_required(roles=['OWNER', 'STAFF', 'SYS_ADMIN'])
def create_category():
    """
    Create a new category
    ---
    tags:
      - Menu
    parameters:
      - in: header
        name: Authorization
        type: string
        required: true
        description: Bearer <token>
      - in: body
        name: body
        schema:
          id: CreateCategoryRequest
          required:
            - name
          properties:
            name:
              type: string
            display_order:
              type: integer
    responses:
      201:
        description: Category created
    """
    data = request.get_json()
    db = next(get_db())
    try:
        req = CreateCategoryRequest(**data)
        
        category_repo = CategoryRepository(db)
        product_repo = ProductRepository(db)
        service = MenuService(category_repo, product_repo)
        
        result = service.create_category(g.tenant_id, req.name, req.display_order)
        db.commit()
        
        return jsonify(result), 201
    except ValidationError as e:
        return jsonify({"error": "Validation Error", "details": e.errors()}), 400
    except Exception as e:
        db.rollback()
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()

@menu_bp.route('/categories', methods=['GET'])
@auth_required()
def get_categories():
    """
    List all categories for the tenant
    ---
    tags:
      - Menu
    parameters:
      - in: header
        name: Authorization
        type: string
        required: true
    responses:
      200:
        description: List of categories
    """
    db = next(get_db())
    try:
        category_repo = CategoryRepository(db)
        product_repo = ProductRepository(db)
        service = MenuService(category_repo, product_repo)
        
        results = service.get_categories(g.tenant_id)
        return jsonify(results), 200
    except Exception as e:
        return jsonify({"error": "Internal Server Error"}), 500
    finally:
        db.close()

@menu_bp.route('/products', methods=['POST'])
@auth_required(roles=['OWNER', 'STAFF', 'SYS_ADMIN'])
def create_product():
    """
    Create a new product
    ---
    tags:
      - Menu
    parameters:
      - in: header
        name: Authorization
        type: string
        required: true
      - in: body
        name: body
        schema:
            id: CreateProductRequest
            required:
                - category_id
                - name
                - price
            properties:
                category_id:
                    type: string
                    format: uuid
                name:
                    type: string
                price:
                    type: number
                description:
                    type: string
                is_available:
                    type: boolean
    responses:
      201:
        description: Product created
    """
    data = request.get_json()
    db = next(get_db())
    try:
        req = CreateProductRequest(**data)
        
        category_repo = CategoryRepository(db)
        product_repo = ProductRepository(db)
        service = MenuService(category_repo, product_repo)
        
        # Note: g.tenant_id comes from token
        result = service.create_product(g.tenant_id, str(req.category_id), req.model_dump())
        db.commit()
        
        return jsonify(result), 201
    except ValidationError as e:
        return jsonify({"error": "Validation Error", "details": e.errors()}), 400
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        db.rollback()
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()

@menu_bp.route('/products', methods=['GET'])
@auth_required()
def get_products():
    """
    List products (optionally filtered by category)
    ---
    tags:
      - Menu
    parameters:
      - in: header
        name: Authorization
        type: string
        required: true
      - in: query
        name: category_id
        type: string
    responses:
      200:
        description: List of products
    """
    category_id = request.args.get('category_id')
    db = next(get_db())
    try:
        category_repo = CategoryRepository(db)
        product_repo = ProductRepository(db)
        service = MenuService(category_repo, product_repo)
        
        results = service.get_products(g.tenant_id, category_id)
        return jsonify(results), 200
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": "Internal Server Error"}), 500
    finally:
        db.close()
