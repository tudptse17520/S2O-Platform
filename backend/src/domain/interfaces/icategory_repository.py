from abc import ABC, abstractmethod
from typing import List, Optional
from ..models.category import Category

class ICategoryRepository(ABC):
    @abstractmethod
    def save(self, category: Category) -> Category:
        pass

    @abstractmethod
    def get_by_id(self, id: str) -> Optional[Category]:
        pass

    @abstractmethod
    def get_all_by_tenant(self, tenant_id: str) -> List[Category]:
        pass
