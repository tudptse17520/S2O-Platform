from flask import Blueprint, request, jsonify, g
from pydantic import BaseModel, Field
from typing import Optional
from ..middleware import auth_required
from ...services.chatbot_service import ChatbotService
from ...infrastructure.services.openai_service import OpenAIService
from ...infrastructure.services.embedding_service import EmbeddingService
from ...infrastructure.repositories.vector_repository import VectorRepository
from ...infrastructure.databases.postgres import get_db
import logging

logger = logging.getLogger(__name__)

chatbot_bp = Blueprint("chatbot", __name__, url_prefix="/chatbot")


class ChatRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=1000)


class IndexDocumentRequest(BaseModel):
    doc_id: str
    text: str
    entity_type: Optional[str] = None
    entity_id: Optional[str] = None


@chatbot_bp.route("/chat", methods=["POST"])
@auth_required()
def chat():
    """
    Ask the AI chatbot a question
    ---
    tags:
      - AI Chatbot
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
            - question
          properties:
            question:
              type: string
              description: The question to ask the chatbot
    responses:
      200:
        description: Chatbot response
        schema:
          type: object
          properties:
            query:
              type: string
            answer:
              type: string
            context:
              type: array
              items:
                type: object
    """
    data = request.get_json()
    db = next(get_db())
    
    try:
        req = ChatRequest(**data)
        
        # Initialize services
        vector_repo = VectorRepository(db)
        openai_service = OpenAIService()
        embed_service = EmbeddingService()
        
        chatbot = ChatbotService(vector_repo, openai_service, embed_service)
        result = chatbot.ask_chatbot(req.question, g.tenant_id)
        
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Chatbot error: {e}")
        return jsonify({
            "query": data.get("question", ""),
            "answer": "I apologize, but I'm having trouble processing your request. Please try again.",
            "error": str(e)
        }), 200  # Return 200 with error message for chatbot
    finally:
        db.close()


@chatbot_bp.route("/index", methods=["POST"])
@auth_required(roles=['OWNER', 'SYS_ADMIN'])
def index_document():
    """
    Index a document for RAG retrieval
    ---
    tags:
      - AI Chatbot
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
            - doc_id
            - text
          properties:
            doc_id:
              type: string
            text:
              type: string
            entity_type:
              type: string
            entity_id:
              type: string
    responses:
      200:
        description: Document indexed successfully
      400:
        description: Indexing failed
    """
    data = request.get_json()
    db = next(get_db())
    
    try:
        req = IndexDocumentRequest(**data)
        
        vector_repo = VectorRepository(db)
        openai_service = OpenAIService()
        embed_service = EmbeddingService()
        
        chatbot = ChatbotService(vector_repo, openai_service, embed_service)
        
        metadata = {
            "text": req.text,
            "tenant_id": g.tenant_id,
            "entity_type": req.entity_type,
            "entity_id": req.entity_id
        }
        
        success = chatbot.index_document(req.doc_id, req.text, metadata)
        
        if success:
            return jsonify({"message": "Document indexed successfully", "doc_id": req.doc_id}), 200
        else:
            return jsonify({"error": "Failed to index document"}), 400
    except Exception as e:
        logger.error(f"Index document error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()
