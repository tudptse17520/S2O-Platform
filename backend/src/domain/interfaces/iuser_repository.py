from abc import ABC, abstractmethod
from typing import List, Optional
from domain.models.user import User


class IUserRepository(ABC):
    """
    Interface for User Repository
    
    Defines contract for user data access operations.
    """
    
    @abstractmethod
    def create(self, user: User) -> User:
        """Create a new user"""
        pass
    
    @abstractmethod
    def get_by_id(self, user_id: str) -> Optional[User]:
        """Get user by ID"""
        pass
    
    @abstractmethod
    def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email address"""
        pass
    
    @abstractmethod
    def get_all(self) -> List[User]:
        """Get all users"""
        pass
    
    @abstractmethod
    def update(self, user_id: str, user: User) -> User:
        """Update user"""
        pass
    
    @abstractmethod
    def delete(self, user_id: str) -> bool:
        """Delete user"""
        pass
    
    @abstractmethod
    def get_by_role(self, role: str) -> List[User]:
        """Get users by role"""
        pass
