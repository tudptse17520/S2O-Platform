from flask import Blueprint, request, jsonify, g
from pydantic import ValidationError
from ..schemas.review_schema import CreateReviewRequest, UpdateReviewRequest
from ..middleware import auth_required
from ...services.review_service import ReviewService
from ...infrastructure.databases.postgres import get_db
from ...infrastructure.repositories import ReviewRepository
import logging

logger = logging.getLogger(__name__)

review_bp = Blueprint("reviews", __name__, url_prefix="/reviews")


@review_bp.route("", methods=["GET"])
@auth_required()
def get_reviews():
    """
    Get all reviews for current tenant
    ---
    tags:
      - Reviews
    parameters:
      - in: header
        name: Authorization
        type: string
        required: true
    responses:
      200:
        description: List of reviews
    """
    db = next(get_db())
    try:
        review_repo = ReviewRepository(db)
        service = ReviewService(review_repo)
        
        reviews = service.get_reviews_by_tenant(g.tenant_id)
        avg_rating = service.get_average_rating(g.tenant_id)
        
        return jsonify({"reviews": reviews, "average_rating": avg_rating}), 200
    except Exception as e:
        logger.error(f"Get reviews error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()


@review_bp.route("/<review_id>", methods=["GET"])
@auth_required()
def get_review(review_id):
    """
    Get review by ID
    ---
    tags:
      - Reviews
    parameters:
      - in: header
        name: Authorization
        type: string
        required: true
      - in: path
        name: review_id
        type: string
        required: true
    responses:
      200:
        description: Review details
      404:
        description: Review not found
    """
    db = next(get_db())
    try:
        review_repo = ReviewRepository(db)
        service = ReviewService(review_repo)
        
        review = service.get_review(review_id)
        if not review:
            return jsonify({"error": "Review not found"}), 404
        return jsonify(review), 200
    except Exception as e:
        logger.error(f"Get review error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()


@review_bp.route("/my", methods=["GET"])
@auth_required()
def get_my_reviews():
    """
    Get current user's reviews
    ---
    tags:
      - Reviews
    parameters:
      - in: header
        name: Authorization
        type: string
        required: true
    responses:
      200:
        description: User's reviews
    """
    db = next(get_db())
    try:
        review_repo = ReviewRepository(db)
        service = ReviewService(review_repo)
        
        reviews = service.get_reviews_by_user(g.user_id)
        return jsonify({"reviews": reviews}), 200
    except Exception as e:
        logger.error(f"Get my reviews error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()


@review_bp.route("", methods=["POST"])
@auth_required()
def create_review():
    """
    Create new review
    ---
    tags:
      - Reviews
    parameters:
      - in: header
        name: Authorization
        type: string
        required: true
      - in: body
        name: body
        schema:
          id: CreateReviewRequest
          required:
            - rating
          properties:
            order_id:
              type: string
            rating:
              type: integer
              minimum: 1
              maximum: 5
            comment:
              type: string
    responses:
      201:
        description: Review created
    """
    data = request.get_json()
    db = next(get_db())
    try:
        req = CreateReviewRequest(**data)
        
        review_repo = ReviewRepository(db)
        service = ReviewService(review_repo)
        
        result = service.create_review(g.user_id, g.tenant_id, req.model_dump())
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
        logger.error(f"Create review error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()


@review_bp.route("/<review_id>", methods=["PUT"])
@auth_required()
def update_review(review_id):
    """
    Update review
    ---
    tags:
      - Reviews
    parameters:
      - in: header
        name: Authorization
        type: string
        required: true
      - in: path
        name: review_id
        type: string
        required: true
      - in: body
        name: body
        schema:
          id: UpdateReviewRequest
          properties:
            rating:
              type: integer
            comment:
              type: string
    responses:
      200:
        description: Review updated
    """
    data = request.get_json()
    db = next(get_db())
    try:
        req = UpdateReviewRequest(**data)
        
        review_repo = ReviewRepository(db)
        service = ReviewService(review_repo)
        
        result = service.update_review(review_id, g.user_id, req.model_dump(exclude_unset=True))
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
        logger.error(f"Update review error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()


@review_bp.route("/<review_id>", methods=["DELETE"])
@auth_required()
def delete_review(review_id):
    """
    Delete review
    ---
    tags:
      - Reviews
    parameters:
      - in: header
        name: Authorization
        type: string
        required: true
      - in: path
        name: review_id
        type: string
        required: true
    responses:
      200:
        description: Review deleted
    """
    db = next(get_db())
    try:
        review_repo = ReviewRepository(db)
        service = ReviewService(review_repo)
        
        deleted = service.delete_review(review_id, g.user_id)
        db.commit()
        
        if deleted:
            return jsonify({"message": "Review deleted"}), 200
        return jsonify({"error": "Review not found"}), 404
    except ValueError as e:
        db.rollback()
        return jsonify({"error": str(e)}), 403
    except Exception as e:
        db.rollback()
        logger.error(f"Delete review error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()
