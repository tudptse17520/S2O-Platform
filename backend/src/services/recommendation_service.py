from typing import List, Dict, Any
from ..domain.interfaces.ivector_repository import IVectorRepository
from ..infrastructure.services.embedding_service import EmbeddingService


class RecommendationService:
    """Service for AI-powered recommendations using vector similarity search"""

    def __init__(self, vector_repo: IVectorRepository, embedding_service: EmbeddingService = None):
        self.vector_repo = vector_repo
        self.embedding_service = embedding_service

    def get_recommendations_by_embedding(
        self, 
        query_embedding: List[float], 
        top_k: int = 5
    ) -> Dict[str, Any]:
        """
        Get recommendations using pre-computed embedding
        """
        results = self.vector_repo.search_vector(query_embedding, top_k)
        return {
            "recommendations": results,
            "count": len(results)
        }

    def get_recommendations_by_text(
        self, 
        query_text: str, 
        top_k: int = 5
    ) -> Dict[str, Any]:
        """
        Get recommendations by generating embedding from text query
        """
        if not self.embedding_service:
            raise ValueError("Embedding service not configured")
        
        query_embedding = self.embedding_service.create_embedding(query_text)
        return self.get_recommendations_by_embedding(query_embedding, top_k)

    def get_similar_products(
        self, 
        product_id: str, 
        product_embedding: List[float],
        top_k: int = 5
    ) -> Dict[str, Any]:
        """
        Get products similar to a given product
        """
        results = self.vector_repo.search_vector(product_embedding, top_k + 1)
        # Filter out the source product
        filtered = [r for r in results if r.get('id') != product_id][:top_k]
        return {
            "source_product_id": product_id,
            "similar_products": filtered,
            "count": len(filtered)
        }

    def get_personalized_recommendations(
        self,
        user_preferences: List[float],
        top_k: int = 10
    ) -> Dict[str, Any]:
        """
        Get personalized recommendations based on user preference vector
        """
        results = self.vector_repo.search_vector(user_preferences, top_k)
        return {
            "personalized_recommendations": results,
            "count": len(results)
        }