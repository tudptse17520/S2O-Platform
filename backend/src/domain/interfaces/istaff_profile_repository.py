from abc import ABC, abstractmethod
from typing import List, Optional
from ..models.staff_profile import StaffProfile


class IStaffProfileRepository(ABC):
    """
    Interface for Staff Profile Repository
    
    Defines contract for staff profile data access operations.
    """
    
    @abstractmethod
    def create(self, staff_profile: StaffProfile) -> StaffProfile:
        """Create a new staff profile"""
        pass
    
    @abstractmethod
    def get_by_user_id(self, user_id: str) -> Optional[StaffProfile]:
        """Get staff profile by user ID"""
        pass
    
    @abstractmethod
    def get_all(self) -> List[StaffProfile]:
        """Get all staff profiles"""
        pass
    
    @abstractmethod
    def get_by_tenant(self, tenant_id: str) -> List[StaffProfile]:
        """Get all staff for a tenant"""
        pass
    
    @abstractmethod
    def get_by_branch(self, branch_id: str) -> List[StaffProfile]:
        """Get all staff for a branch"""
        pass
    
    @abstractmethod
    def update(self, user_id: str, staff_profile: StaffProfile) -> StaffProfile:
        """Update staff profile"""
        pass
    
    @abstractmethod
    def delete(self, user_id: str) -> bool:
        """Delete staff profile"""
        pass
    
    @abstractmethod
    def get_by_position(self, tenant_id: str, position: str) -> List[StaffProfile]:
        """Get staff by position"""
        pass
