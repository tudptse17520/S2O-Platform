from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from sqlalchemy import text
from ...domain.interfaces.ivector_repository import IVectorRepository


class VectorRepository(IVectorRepository):
    """
    Vector repository for similarity search using pgvector
    Requires PostgreSQL with pgvector extension installed
    """
    
    def __init__(self, db: Session):
        self.db = db

    def upsert_vector(self, vector_id: str, embedding: List[float], metadata: Dict[str, Any]) -> None:
        """
        Insert or update a vector with metadata
        """
        sql = text("""
            INSERT INTO embeddings (id, text, embedding, metadata)
            VALUES (:id, :text, :embedding, :metadata)
            ON CONFLICT (id) DO UPDATE SET
                text = EXCLUDED.text,
                embedding = EXCLUDED.embedding,
                metadata = EXCLUDED.metadata,
                updated_at = NOW()
        """)
        
        self.db.execute(sql, {
            "id": vector_id,
            "text": metadata.get("text", ""),
            "embedding": embedding,
            "metadata": str(metadata)
        })
        self.db.commit()

    def search_vector(self, embedding: List[float], top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Search for similar vectors using cosine distance
        Returns list of matching documents with similarity scores
        """
        sql = text("""
            SELECT id, text, metadata, 
                   1 - (embedding <=> :embedding::vector) as similarity
            FROM embeddings
            ORDER BY embedding <=> :embedding::vector
            LIMIT :top_k
        """)

        try:
            result = self.db.execute(sql, {
                "embedding": embedding,
                "top_k": top_k
            })
            
            rows = result.fetchall()
            return [
                {
                    "id": row[0],
                    "text": row[1],
                    "metadata": row[2],
                    "similarity": float(row[3]) if row[3] else 0.0
                }
                for row in rows
            ]
        except Exception as e:
            # If pgvector is not installed or table doesn't exist, return empty
            return []

    def delete_vector(self, vector_id: str) -> bool:
        """Delete a vector by ID"""
        sql = text("DELETE FROM embeddings WHERE id = :id")
        result = self.db.execute(sql, {"id": vector_id})
        self.db.commit()
        return result.rowcount > 0

    def get_vector(self, vector_id: str) -> Optional[Dict[str, Any]]:
        """Get a single vector by ID"""
        sql = text("SELECT id, text, embedding, metadata FROM embeddings WHERE id = :id")
        result = self.db.execute(sql, {"id": vector_id})
        row = result.fetchone()
        
        if row:
            return {
                "id": row[0],
                "text": row[1],
                "embedding": row[2],
                "metadata": row[3]
            }
        return None
