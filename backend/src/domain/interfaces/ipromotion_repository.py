from abc import ABC, abstractmethod
from typing import List, Optional
from domain.models.promotion import Promotion


class IPromotionRepository(ABC):
    """
    Interface for Promotion Repository
    
    Defines contract for promotion data access operations.
    """
    
    @abstractmethod
    def create(self, promotion: Promotion) -> Promotion:
        """Create a new promotion"""
        pass
    
    @abstractmethod
    def get_by_id(self, promotion_id: str) -> Optional[Promotion]:
        """Get promotion by ID"""
        pass
    
    @abstractmethod
    def get_all(self) -> List[Promotion]:
        """Get all promotions"""
        pass
    
    @abstractmethod
    def get_by_tenant(self, tenant_id: str) -> List[Promotion]:
        """Get all promotions for a tenant"""
        pass
    
    @abstractmethod
    def get_by_code(self, tenant_id: str, code: str) -> Optional[Promotion]:
        """Get promotion by code for a tenant"""
        pass
    
    @abstractmethod
    def update(self, promotion_id: str, promotion: Promotion) -> Promotion:
        """Update promotion"""
        pass
    
    @abstractmethod
    def delete(self, promotion_id: str) -> bool:
        """Delete promotion"""
        pass
    
    @abstractmethod
    def get_active_promotions(self, tenant_id: str) -> List[Promotion]:
        """Get all active promotions for a tenant"""
        pass
