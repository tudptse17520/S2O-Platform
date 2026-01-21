from typing import Optional
from enum import Enum


class StaffPosition(str, Enum):
    """Enum for staff positions"""
    MANAGER = "MANAGER"
    CHEF = "CHEF"
    CASHIER = "CASHIER"
    WAITER = "WAITER"


class StaffProfile:
    """
    Domain Model for Staff Profile
    
    Represents a staff profile linked to a User.
    One-to-One relationship with User.
    Attributes map to the 'staff_profiles' table in DRD.
    """
    
    def __init__(
        self,
        user_id: str,
        tenant_id: str,
        branch_id: str,
        position: str,
        is_active: bool = True
    ):
        self.user_id = user_id
        self.tenant_id = tenant_id
        self.branch_id = branch_id
        self.position = position
        self.is_active = is_active
    
    def activate(self) -> None:
        """Activate staff account"""
        self.is_active = True
    
    def deactivate(self) -> None:
        """Deactivate staff account"""
        self.is_active = False
    
    def change_position(self, new_position: str) -> None:
        """Change staff position"""
        self.position = new_position
    
    def change_branch(self, new_branch_id: str) -> None:
        """Transfer staff to different branch"""
        self.branch_id = new_branch_id
    
    def is_valid(self) -> bool:
        """Validate staff profile data"""
        return (
            self.user_id 
            and self.tenant_id 
            and self.branch_id 
            and self.position
        )
    
    def __repr__(self) -> str:
        return f"<StaffProfile user_id={self.user_id} position={self.position} active={self.is_active}>"
