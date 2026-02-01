from abc import ABC, abstractmethod
from typing import List, Optional
from ..models.category import Category


class ICategoryRepository(ABC):
    @abstractmethod
    def save(self, category: Category) -> Category:
        """Save or update a category"""
        pass

    @abstractmethod
    def get_by_id(self, id: str) -> Optional[Category]:
        """Get category by ID"""
        pass

    @abstractmethod
    def get_all_by_tenant(self, tenant_id: str) -> List[Category]:
        """Get all categories for a tenant"""
        pass

    @abstractmethod
    def delete(self, category_id: str) -> bool:
        """Delete category by ID"""
        pass
