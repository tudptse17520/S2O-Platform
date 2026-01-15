from fastapi import APIRouter
from domain.services.recommendation_service import RecommendationService
from infrastructure.embedding_service import EmbeddingService

router = APIRouter()

def inject_dependencies():
    from infrastructure.vector_repository import VectorRepository
    from infrastructure.database_qdrant import QdrantDB

    db = QdrantDB()
    repo = VectorRepository(db)
    embed = EmbeddingService()
    return RecommendationService(repo), embed

@router.post("/recommend")
def recommend(payload: dict):
    service, embed = inject_dependencies()
    text = payload.get("text", "")
    embedding = embed.create_embedding(text)
    return service.get_recommendation(embedding)
