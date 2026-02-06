from flask import Blueprint, request, jsonify, g
from pydantic import BaseModel, Field
from typing import List, Optional
from ..middleware import auth_required
from ...services.recommendation_service import RecommendationService
from ...infrastructure.services.embedding_service import EmbeddingService
from ...infrastructure.repositories.vector_repository import VectorRepository
from ...infrastructure.databases.postgres import get_db
import logging

logger = logging.getLogger(__name__)

recommendation_bp = Blueprint("recommendations", __name__, url_prefix="/recommendations")


class TextRecommendationRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=500)
    top_k: int = Field(default=5, ge=1, le=20)


class EmbeddingRecommendationRequest(BaseModel):
    embedding: List[float]
    top_k: int = Field(default=5, ge=1, le=20)


class SimilarProductRequest(BaseModel):
    product_id: str
    top_k: int = Field(default=5, ge=1, le=20)


@recommendation_bp.route("/by-text", methods=["POST"])
@auth_required()
def get_recommendations_by_text():
    """
    Get recommendations based on text query
    ---
    tags:
      - AI Recommendations
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
            - text
          properties:
            text:
              type: string
              description: Text query for semantic search
            top_k:
              type: integer
              default: 5
              description: Number of recommendations to return
    responses:
      200:
        description: List of recommendations
    """
    data = request.get_json()
    db = next(get_db())
    
    try:
        req = TextRecommendationRequest(**data)
        
        vector_repo = VectorRepository(db)
        embed_service = EmbeddingService()
        
        service = RecommendationService(vector_repo, embed_service)
        result = service.get_recommendations_by_text(req.text, req.top_k)
        
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Recommendation error: {e}")
        return jsonify({"error": str(e), "recommendations": []}), 200
    finally:
        db.close()


@recommendation_bp.route("/by-embedding", methods=["POST"])
@auth_required()
def get_recommendations_by_embedding():
    """
    Get recommendations based on pre-computed embedding
    ---
    tags:
      - AI Recommendations
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
            - embedding
          properties:
            embedding:
              type: array
              items:
                type: number
              description: Pre-computed embedding vector
            top_k:
              type: integer
              default: 5
    responses:
      200:
        description: List of recommendations
    """
    data = request.get_json()
    db = next(get_db())
    
    try:
        req = EmbeddingRecommendationRequest(**data)
        
        vector_repo = VectorRepository(db)
        service = RecommendationService(vector_repo)
        result = service.get_recommendations_by_embedding(req.embedding, req.top_k)
        
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Recommendation error: {e}")
        return jsonify({"error": str(e), "recommendations": []}), 200
    finally:
        db.close()


@recommendation_bp.route("/similar-products/<product_id>", methods=["GET"])
@auth_required()
def get_similar_products(product_id):
    """
    Get products similar to a given product
    ---
    tags:
      - AI Recommendations
    parameters:
      - in: header
        name: Authorization
        type: string
        required: true
      - in: path
        name: product_id
        type: string
        required: true
      - in: query
        name: top_k
        type: integer
        default: 5
    responses:
      200:
        description: List of similar products
    """
    db = next(get_db())
    
    try:
        top_k = request.args.get('top_k', 5, type=int)
        
        vector_repo = VectorRepository(db)
        embed_service = EmbeddingService()
        
        # Get the product embedding (in production, this would come from the database)
        # For now, we'll create an embedding from the product_id as a placeholder
        product_embedding = embed_service.create_embedding(f"product:{product_id}")
        
        service = RecommendationService(vector_repo, embed_service)
        result = service.get_similar_products(product_id, product_embedding, top_k)
        
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Similar products error: {e}")
        return jsonify({"error": str(e), "similar_products": []}), 200
    finally:
        db.close()


@recommendation_bp.route("/personalized", methods=["GET"])
@auth_required()
def get_personalized_recommendations():
    """
    Get personalized recommendations for current user
    ---
    tags:
      - AI Recommendations
    parameters:
      - in: header
        name: Authorization
        type: string
        required: true
      - in: query
        name: top_k
        type: integer
        default: 10
    responses:
      200:
        description: Personalized recommendations
    """
    db = next(get_db())
    
    try:
        top_k = request.args.get('top_k', 10, type=int)
        
        vector_repo = VectorRepository(db)
        embed_service = EmbeddingService()
        
        # Create a user preference embedding (in production, this would be based on user history)
        # For now, we use the user_id to create a deterministic embedding
        user_preference = embed_service.create_embedding(f"user:{g.user_id}")
        
        service = RecommendationService(vector_repo, embed_service)
        result = service.get_personalized_recommendations(user_preference, top_k)
        
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Personalized recommendation error: {e}")
        return jsonify({"error": str(e), "personalized_recommendations": []}), 200
    finally:
        db.close()
