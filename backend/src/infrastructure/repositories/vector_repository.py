from domain.interfaces.ivector_repository import IVectorRepository
from sqlalchemy.orm import Session

class VectorRepository(IVectorRepository):
    def __init__(self, db: Session):
        self.db = db

    def save_vector(self, text: str, embedding: list):
        sql = """
            INSERT INTO embeddings (text, embedding)
            VALUES (:text, :embedding)
        """

        self.db.execute(sql, {"text": text, "embedding": embedding})
        self.db.commit()

    def search_vector(self, embedding: list, top_k: int = 5):
        sql = """
            SELECT text, embedding
            FROM embeddings
            ORDER BY embedding <-> :embedding
            LIMIT :top_k
        """

        result = self.db.execute(sql, {
            "embedding": embedding,
            "top_k": top_k
        })

        return result.fetchall()

