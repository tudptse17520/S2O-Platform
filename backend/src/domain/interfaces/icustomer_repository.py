from abc import ABC, abstractmethod
from typing import List, Optional
from domain.models.customer import Customer


class ICustomerRepository(ABC):
    """
    Interface for Customer Repository
    
    Defines contract for customer profile data access operations.
    """
    
    @abstractmethod
    def create(self, customer: Customer) -> Customer:
        """Create a new customer profile"""
        pass
    
    @abstractmethod
    def get_by_user_id(self, user_id: str) -> Optional[Customer]:
        """Get customer profile by user ID"""
        pass
    
    @abstractmethod
    def get_all(self) -> List[Customer]:
        """Get all customer profiles"""
        pass
    
    @abstractmethod
    def update(self, user_id: str, customer: Customer) -> Customer:
        """Update customer profile"""
        pass
    
    @abstractmethod
    def delete(self, user_id: str) -> bool:
        """Delete customer profile"""
        pass
    
    @abstractmethod
    def add_loyalty_points(self, user_id: str, points: int) -> Customer:
        """Add loyalty points to customer"""
        pass
    
    @abstractmethod
    def redeem_loyalty_points(self, user_id: str, points: int) -> bool:
        """Redeem loyalty points from customer"""
        pass
