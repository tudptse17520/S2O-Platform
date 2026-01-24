from typing import Optional
from datetime import datetime


class Category:
    """
    Domain Model for Category
    
    Represents a menu category/section.
    Attributes map to the 'categories' table in DRD.
    """
    
    def __init__(
        self,
        id: str,
        tenant_id: str,
        name: str,
        display_order: int = 0,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.tenant_id = tenant_id
        self.name = name
        self.display_order = display_order
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
    
    def is_valid(self) -> bool:
        """Validate category data"""
        return self.name and self.tenant_id
    
    def __repr__(self) -> str:
        return f"<Category id={self.id} name={self.name}>"
