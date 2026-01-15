from infrastructure.openai_service import OpenAIService
from infrastructure.embedding_service import EmbeddingService
from domain.interfaces.ivector_repository import IVectorRepository

class ChatbotService:

    def __init__(self, vector_repo: IVectorRepository, openai_service: OpenAIService, embed_service: EmbeddingService):
        self.vector_repo = vector_repo
        self.openai = openai_service
        self.embedding = embed_service

    def ask_chatbot(self, query: str):
        emb = self.embedding.create_embedding(query)
        context_docs = self.vector_repo.search_vector(emb)

        final_answer = self.openai.generate_answer(query, context_docs)

        return {
            "query": query,
            "context": context_docs,
            "answer": final_answer
        }