from abc import ABC, abstractmethod
from typing import List, Dict, Any

class IVectorRepository(ABC):

    @abstractmethod
    def upsert_vector(self, vector_id: str, embedding: List[float], metadata: Dict[str, Any]):
        pass

    @abstractmethod
    def search_vector(self, embedding: List[float], top_k: int = 5) -> List[Dict[str, Any]]:
        pass