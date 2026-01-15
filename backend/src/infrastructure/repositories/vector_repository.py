from domain.interfaces.ivector_repository import IVectorRepository

class VectorRepository(IVectorRepository):

    def __init__(self, db):
        self.db = db

    def upsert_vector(self, vector_id, embedding, metadata):
        record = {
            "id": vector_id,
            "embedding": embedding,
            "metadata": metadata
        }
        self.db.upsert(record)
        return record

    def search_vector(self, embedding, top_k=5):
        return self.db.search(embedding, top_k)
