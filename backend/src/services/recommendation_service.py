from typing import List
from domain.interfaces.ivector_repository import IVectorRepository

class RecommendationService:

    def __init__(self, vector_repo: IVectorRepository):
        self.vector_repo = vector_repo

    def get_recommendation(self, query_embedding: List[float], top_k: int = 5):
        """
        Gọi repository để tìm kết quả
        """
        results = self.vector_repo.search_vector(query_embedding, top_k)
        return {
            "query_embedding": query_embedding,
            "recommendations": results
        }