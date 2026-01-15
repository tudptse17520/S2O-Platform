from fastapi import APIRouter
from infrastructure.openai_service import OpenAIService
from infrastructure.embedding_service import EmbeddingService
from infrastructure.vector_repository import VectorRepository
from infrastructure.database_postgres import PostgresDB
from services.chatbot_service import ChatbotService

router = APIRouter()

@router.post("/chat")
def chat(payload: dict):
    question = payload.get("question", "")

    db = PostgresDB()
    repo = VectorRepository(db)
    openai_service = OpenAIService()
    embed_service = EmbeddingService()

    chatbot = ChatbotService(repo, openai_service, embed_service)
    return chatbot.ask_chatbot(question)
