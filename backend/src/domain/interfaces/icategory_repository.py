from abc import ABC, abstractmethod
from typing import List, Optional
from domain.models.category import Category


class ICategoryRepository(ABC):
    """
    Interface for Category Repository
    
    Defines contract for category data access operations.
    """
    
    @abstractmethod
    def create(self, category: Category) -> Category:
        """Create a new category"""
        pass
    
    @abstractmethod
    def get_by_id(self, category_id: str) -> Optional[Category]:
        """Get category by ID"""
        pass
    
    @abstractmethod
    def get_all(self) -> List[Category]:
        """Get all categories"""
        pass
    
    @abstractmethod
    def get_by_tenant(self, tenant_id: str) -> List[Category]:
        """Get all categories for a tenant"""
        pass
    
    @abstractmethod
    def update(self, category_id: str, category: Category) -> Category:
        """Update category"""
        pass
    
    @abstractmethod
    def delete(self, category_id: str) -> bool:
        """Delete category"""
        pass
    
    @abstractmethod
    def get_by_name(self, tenant_id: str, name: str) -> Optional[Category]:
        """Get category by name for a tenant"""
        pass
