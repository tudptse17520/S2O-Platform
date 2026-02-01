from flask import Blueprint, request, jsonify, g
from pydantic import ValidationError
from ..schemas.customer_schema import CreateCustomerRequest, UpdateCustomerRequest, AddLoyaltyPointsRequest, RedeemLoyaltyPointsRequest
from ..middleware import auth_required
from ...services.customer_service import CustomerService
from ...infrastructure.databases.postgres import get_db
from ...infrastructure.repositories.customer_repository import CustomerRepository
import logging

logger = logging.getLogger(__name__)

customer_bp = Blueprint("customers", __name__, url_prefix="/customers")


@customer_bp.route("", methods=["GET"])
@auth_required(roles=['OWNER', 'STAFF', 'SYS_ADMIN'])
def get_customers():
    """
    Get all customers for current tenant
    ---
    tags:
      - Customers
    parameters:
      - in: header
        name: Authorization
        type: string
        required: true
    responses:
      200:
        description: List of customers
    """
    db = next(get_db())
    try:
        customer_repo = CustomerRepository(db)
        service = CustomerService(customer_repo)
        
        customers = service.get_customers_by_tenant(g.tenant_id)
        return jsonify({"customers": customers}), 200
    except Exception as e:
        logger.error(f"Get customers error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()


@customer_bp.route("/me", methods=["GET"])
@auth_required()
def get_my_profile():
    """
    Get current user's customer profile
    ---
    tags:
      - Customers
    parameters:
      - in: header
        name: Authorization
        type: string
        required: true
    responses:
      200:
        description: Customer profile
      404:
        description: Profile not found
    """
    db = next(get_db())
    try:
        customer_repo = CustomerRepository(db)
        service = CustomerService(customer_repo)
        
        customer = service.get_customer(g.user_id)
        if not customer:
            return jsonify({"error": "Customer profile not found"}), 404
        return jsonify(customer), 200
    except Exception as e:
        logger.error(f"Get my profile error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()


@customer_bp.route("/<user_id>", methods=["GET"])
@auth_required(roles=['OWNER', 'STAFF', 'SYS_ADMIN'])
def get_customer(user_id):
    """
    Get customer by user ID
    ---
    tags:
      - Customers
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
        description: Customer details
      404:
        description: Customer not found
    """
    db = next(get_db())
    try:
        customer_repo = CustomerRepository(db)
        service = CustomerService(customer_repo)
        
        customer = service.get_customer(user_id)
        if not customer:
            return jsonify({"error": "Customer not found"}), 404
        return jsonify(customer), 200
    except Exception as e:
        logger.error(f"Get customer error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()


@customer_bp.route("", methods=["POST"])
@auth_required()
def create_customer():
    """
    Create customer profile for current user
    ---
    tags:
      - Customers
    parameters:
      - in: header
        name: Authorization
        type: string
        required: true
      - in: body
        name: body
        schema:
          id: CreateCustomerRequest
          properties:
            phone_number:
              type: string
    responses:
      201:
        description: Customer created
    """
    data = request.get_json() or {}
    db = next(get_db())
    try:
        req = CreateCustomerRequest(**data)
        
        customer_repo = CustomerRepository(db)
        service = CustomerService(customer_repo)
        
        result = service.create_customer(g.user_id, g.tenant_id, req.model_dump())
        db.commit()
        
        return jsonify(result), 201
    except ValidationError as e:
        db.rollback()
        return jsonify({"error": "Validation Error", "details": e.errors()}), 400
    except Exception as e:
        db.rollback()
        logger.error(f"Create customer error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()


@customer_bp.route("/me", methods=["PUT"])
@auth_required()
def update_my_profile():
    """
    Update current user's customer profile
    ---
    tags:
      - Customers
    parameters:
      - in: header
        name: Authorization
        type: string
        required: true
      - in: body
        name: body
        schema:
          id: UpdateCustomerRequest
          properties:
            phone_number:
              type: string
    responses:
      200:
        description: Profile updated
    """
    data = request.get_json()
    db = next(get_db())
    try:
        req = UpdateCustomerRequest(**data)
        
        customer_repo = CustomerRepository(db)
        service = CustomerService(customer_repo)
        
        result = service.update_customer(g.user_id, req.model_dump(exclude_unset=True))
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
        logger.error(f"Update my profile error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()


@customer_bp.route("/<user_id>/loyalty/add", methods=["POST"])
@auth_required(roles=['OWNER', 'STAFF', 'SYS_ADMIN'])
def add_loyalty_points(user_id):
    """
    Add loyalty points to customer
    ---
    tags:
      - Customers
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
          id: AddLoyaltyPointsRequest
          required:
            - points
          properties:
            points:
              type: integer
    responses:
      200:
        description: Points added
    """
    data = request.get_json()
    db = next(get_db())
    try:
        req = AddLoyaltyPointsRequest(**data)
        
        customer_repo = CustomerRepository(db)
        service = CustomerService(customer_repo)
        
        result = service.add_loyalty_points(user_id, req.points)
        db.commit()
        
        return jsonify(result), 200
    except ValidationError as e:
        db.rollback()
        return jsonify({"error": "Validation Error", "details": e.errors()}), 400
    except ValueError as e:
        db.rollback()
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        db.rollback()
        logger.error(f"Add loyalty points error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()


@customer_bp.route("/<user_id>/loyalty/redeem", methods=["POST"])
@auth_required()
def redeem_loyalty_points(user_id):
    """
    Redeem loyalty points
    ---
    tags:
      - Customers
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
          id: RedeemLoyaltyPointsRequest
          required:
            - points
          properties:
            points:
              type: integer
    responses:
      200:
        description: Points redeemed
    """
    data = request.get_json()
    db = next(get_db())
    try:
        req = RedeemLoyaltyPointsRequest(**data)
        
        customer_repo = CustomerRepository(db)
        service = CustomerService(customer_repo)
        
        result = service.redeem_loyalty_points(user_id, req.points)
        db.commit()
        
        return jsonify(result), 200
    except ValidationError as e:
        db.rollback()
        return jsonify({"error": "Validation Error", "details": e.errors()}), 400
    except ValueError as e:
        db.rollback()
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        db.rollback()
        logger.error(f"Redeem loyalty points error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()
