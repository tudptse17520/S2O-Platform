from typing import Dict, Any
from ..infrastructure.services.openai_service import OpenAIService
from ..infrastructure.services.embedding_service import EmbeddingService
from ..domain.interfaces.ivector_repository import IVectorRepository


class ChatbotService:
    """Service for AI-powered chatbot using RAG (Retrieval Augmented Generation)"""

    def __init__(
        self, 
        vector_repo: IVectorRepository, 
        openai_service: OpenAIService, 
        embed_service: EmbeddingService
    ):
        self.vector_repo = vector_repo
        self.openai = openai_service
        self.embedding = embed_service

    def ask_chatbot(self, query: str, tenant_id: str = None) -> Dict[str, Any]:
        """
        Process a user query using RAG:
        1. Create embedding of the query
        2. Search for relevant context documents
        3. Generate answer using LLM with context
        """
        # Create embedding for the query
        query_embedding = self.embedding.create_embedding(query)
        
        # Search for relevant context documents
        context_docs = self.vector_repo.search_vector(query_embedding, top_k=5)
        
        # Generate answer using OpenAI with context
        final_answer = self.openai.generate_answer(query, context_docs)

        return {
            "query": query,
            "context": context_docs,
            "answer": final_answer
        }

    def index_document(self, doc_id: str, text: str, metadata: Dict[str, Any] = None) -> bool:
        """Index a document for RAG retrieval"""
        try:
            embedding = self.embedding.create_embedding(text)
            self.vector_repo.upsert_vector(doc_id, embedding, metadata or {"text": text})
            return True
        except Exception:
            return False