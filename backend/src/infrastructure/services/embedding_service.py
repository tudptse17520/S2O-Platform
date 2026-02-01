import os
from typing import List, Optional

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False


class EmbeddingService:
    """
    Service for creating text embeddings using OpenAI
    Used for semantic search and recommendations
    """
    
    def __init__(self, api_key: str = None, model: str = "text-embedding-3-small"):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model
        self._client = None
        # Embedding dimensions for different models
        self.dimensions = {
            "text-embedding-3-small": 1536,
            "text-embedding-3-large": 3072,
            "text-embedding-ada-002": 1536
        }
        
    @property
    def client(self):
        """Lazy initialization of OpenAI client"""
        if self._client is None and OPENAI_AVAILABLE and self.api_key:
            self._client = OpenAI(api_key=self.api_key)
        return self._client

    def create_embedding(self, text: str) -> List[float]:
        """
        Create embedding vector for text
        Returns a list of floats representing the semantic meaning
        """
        if not self.client:
            # Return dummy embedding when OpenAI is not available
            return self._create_dummy_embedding(text)
        
        try:
            # Clean and truncate text if needed
            clean_text = self._preprocess_text(text)
            
            response = self.client.embeddings.create(
                model=self.model,
                input=clean_text
            )
            return response.data[0].embedding
        except Exception as e:
            # Fallback to dummy embedding on error
            print(f"Embedding error: {e}")
            return self._create_dummy_embedding(text)

    def create_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        """
        Create embeddings for multiple texts in a single API call
        More efficient for bulk operations
        """
        if not self.client:
            return [self._create_dummy_embedding(t) for t in texts]
        
        try:
            clean_texts = [self._preprocess_text(t) for t in texts]
            
            response = self.client.embeddings.create(
                model=self.model,
                input=clean_texts
            )
            return [item.embedding for item in response.data]
        except Exception as e:
            print(f"Batch embedding error: {e}")
            return [self._create_dummy_embedding(t) for t in texts]

    def get_embedding_dimension(self) -> int:
        """Get the dimension of embeddings for current model"""
        return self.dimensions.get(self.model, 1536)

    def _preprocess_text(self, text: str, max_tokens: int = 8000) -> str:
        """Preprocess text for embedding"""
        # Remove excessive whitespace
        clean = " ".join(text.split())
        # Truncate if too long (rough estimate: 4 chars per token)
        max_chars = max_tokens * 4
        if len(clean) > max_chars:
            clean = clean[:max_chars]
        return clean

    def _create_dummy_embedding(self, text: str) -> List[float]:
        """
        Create a dummy embedding when OpenAI is not available
        Uses simple hash-based approach for testing
        """
        import hashlib
        
        dimension = self.get_embedding_dimension()
        
        # Create deterministic pseudo-random embedding from text hash
        text_hash = hashlib.sha256(text.encode()).hexdigest()
        
        embedding = []
        for i in range(dimension):
            # Use different parts of the hash to generate values
            idx = (i * 2) % len(text_hash)
            value = int(text_hash[idx:idx+2], 16) / 255.0 - 0.5
            embedding.append(value)
        
        # Normalize to unit vector
        magnitude = sum(x**2 for x in embedding) ** 0.5
        if magnitude > 0:
            embedding = [x / magnitude for x in embedding]
        
        return embedding
