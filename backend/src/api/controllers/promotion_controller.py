from flask import Blueprint, request, jsonify, g
from pydantic import ValidationError
from ..schemas.promotion_schema import CreatePromotionRequest, UpdatePromotionRequest, ApplyPromotionRequest
from ..middleware import auth_required
from ...services.promotion_service import PromotionService
from ...infrastructure.databases.postgres import get_db
from ...infrastructure.repositories import PromotionRepository
import logging

logger = logging.getLogger(__name__)

promotion_bp = Blueprint("promotions", __name__, url_prefix="/promotions")


@promotion_bp.route("", methods=["GET"])
@auth_required()
def get_promotions():
    """
    Get all promotions for current tenant
    ---
    tags:
      - Promotions
    parameters:
      - in: header
        name: Authorization
        type: string
        required: true
      - in: query
        name: active
        type: boolean
        description: Filter active promotions only
    responses:
      200:
        description: List of promotions
    """
    db = next(get_db())
    try:
        active_only = request.args.get('active', 'false').lower() == 'true'
        
        promotion_repo = PromotionRepository(db)
        service = PromotionService(promotion_repo)
        
        if active_only:
            promotions = service.get_active_promotions(g.tenant_id)
        else:
            promotions = service.get_promotions_by_tenant(g.tenant_id)
        
        return jsonify({"promotions": promotions}), 200
    except Exception as e:
        logger.error(f"Get promotions error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()


@promotion_bp.route("/<promotion_id>", methods=["GET"])
@auth_required()
def get_promotion(promotion_id):
    """
    Get promotion by ID
    ---
    tags:
      - Promotions
    parameters:
      - in: header
        name: Authorization
        type: string
        required: true
      - in: path
        name: promotion_id
        type: string
        required: true
    responses:
      200:
        description: Promotion details
      404:
        description: Promotion not found
    """
    db = next(get_db())
    try:
        promotion_repo = PromotionRepository(db)
        service = PromotionService(promotion_repo)
        
        promotion = service.get_promotion(promotion_id)
        if not promotion:
            return jsonify({"error": "Promotion not found"}), 404
        return jsonify(promotion), 200
    except Exception as e:
        logger.error(f"Get promotion error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()


@promotion_bp.route("/code/<code>", methods=["GET"])
@auth_required()
def get_promotion_by_code(code):
    """
    Get promotion by code
    ---
    tags:
      - Promotions
    parameters:
      - in: header
        name: Authorization
        type: string
        required: true
      - in: path
        name: code
        type: string
        required: true
    responses:
      200:
        description: Promotion details
      404:
        description: Promotion not found
    """
    db = next(get_db())
    try:
        promotion_repo = PromotionRepository(db)
        service = PromotionService(promotion_repo)
        
        promotion = service.get_promotion_by_code(g.tenant_id, code)
        if not promotion:
            return jsonify({"error": "Promotion not found"}), 404
        return jsonify(promotion), 200
    except Exception as e:
        logger.error(f"Get promotion by code error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()


@promotion_bp.route("", methods=["POST"])
@auth_required(roles=['OWNER', 'SYS_ADMIN'])
def create_promotion():
    """
    Create new promotion
    ---
    tags:
      - Promotions
    parameters:
      - in: header
        name: Authorization
        type: string
        required: true
      - in: body
        name: body
        schema:
          id: CreatePromotionRequest
          required:
            - code
            - type
            - value
            - start_date
            - end_date
          properties:
            code:
              type: string
            type:
              type: string
              description: PERCENTAGE, FIXED_AMOUNT, BUY_ONE_GET_ONE
            value:
              type: number
            start_date:
              type: string
            end_date:
              type: string
    responses:
      201:
        description: Promotion created
    """
    data = request.get_json()
    db = next(get_db())
    try:
        req = CreatePromotionRequest(**data)
        
        promotion_repo = PromotionRepository(db)
        service = PromotionService(promotion_repo)
        
        result = service.create_promotion(g.tenant_id, req.model_dump())
        db.commit()
        
        return jsonify(result), 201
    except ValidationError as e:
        db.rollback()
        return jsonify({"error": "Validation Error", "details": e.errors()}), 400
    except Exception as e:
        db.rollback()
        logger.error(f"Create promotion error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()


@promotion_bp.route("/apply", methods=["POST"])
@auth_required()
def apply_promotion():
    """
    Apply promotion code to calculate discount
    ---
    tags:
      - Promotions
    parameters:
      - in: header
        name: Authorization
        type: string
        required: true
      - in: body
        name: body
        schema:
          id: ApplyPromotionRequest
          required:
            - code
            - amount
          properties:
            code:
              type: string
            amount:
              type: number
    responses:
      200:
        description: Discount calculated
    """
    data = request.get_json()
    db = next(get_db())
    try:
        req = ApplyPromotionRequest(**data)
        
        promotion_repo = PromotionRepository(db)
        service = PromotionService(promotion_repo)
        
        result = service.apply_promotion(g.tenant_id, req.code, req.amount)
        
        return jsonify(result), 200
    except ValidationError as e:
        return jsonify({"error": "Validation Error", "details": e.errors()}), 400
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logger.error(f"Apply promotion error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()


@promotion_bp.route("/<promotion_id>", methods=["PUT"])
@auth_required(roles=['OWNER', 'SYS_ADMIN'])
def update_promotion(promotion_id):
    """
    Update promotion
    ---
    tags:
      - Promotions
    parameters:
      - in: header
        name: Authorization
        type: string
        required: true
      - in: path
        name: promotion_id
        type: string
        required: true
      - in: body
        name: body
        schema:
          id: UpdatePromotionRequest
          properties:
            code:
              type: string
            type:
              type: string
            value:
              type: number
            start_date:
              type: string
            end_date:
              type: string
    responses:
      200:
        description: Promotion updated
    """
    data = request.get_json()
    db = next(get_db())
    try:
        req = UpdatePromotionRequest(**data)
        
        promotion_repo = PromotionRepository(db)
        service = PromotionService(promotion_repo)
        
        result = service.update_promotion(promotion_id, req.model_dump(exclude_unset=True))
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
        logger.error(f"Update promotion error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()


@promotion_bp.route("/<promotion_id>", methods=["DELETE"])
@auth_required(roles=['OWNER', 'SYS_ADMIN'])
def delete_promotion(promotion_id):
    """
    Delete promotion
    ---
    tags:
      - Promotions
    parameters:
      - in: header
        name: Authorization
        type: string
        required: true
      - in: path
        name: promotion_id
        type: string
        required: true
    responses:
      200:
        description: Promotion deleted
    """
    db = next(get_db())
    try:
        promotion_repo = PromotionRepository(db)
        service = PromotionService(promotion_repo)
        
        deleted = service.delete_promotion(promotion_id)
        db.commit()
        
        if deleted:
            return jsonify({"message": "Promotion deleted"}), 200
        return jsonify({"error": "Promotion not found"}), 404
    except Exception as e:
        db.rollback()
        logger.error(f"Delete promotion error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()
