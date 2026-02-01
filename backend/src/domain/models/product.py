from typing import Optional
from datetime import datetime


class Product:
    """
    Domain Model for Product (Menu Item)
    
    Represents a product/menu item in the system.
    Attributes map to the 'products' table in DRD.
    """
    
    def __init__(
        self,
        id: str,
        tenant_id: str,
        category_id: str,
        name: str,
        description: Optional[str],
        price: float,
        image_url: Optional[str],
        is_available: bool,
        embedding_vector: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.tenant_id = tenant_id
        self.category_id = category_id
        self.name = name
        self.description = description
        self.price = price
        self.image_url = image_url
        self.is_available = is_available
        self.embedding_vector = embedding_vector
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
    
    def is_valid(self) -> bool:
        """Validate product data"""
        return (
            self.name 
            and self.price > 0 
            and self.tenant_id 
            and self.category_id
        )
    
    def mark_available(self) -> None:
        """Mark product as available"""
        self.is_available = True
        self.updated_at = datetime.utcnow()
    
    def mark_unavailable(self) -> None:
        """Mark product as unavailable"""
        self.is_available = False
        self.updated_at = datetime.utcnow()
    
    def __repr__(self) -> str:
        return f"<Product id={self.id} name={self.name} price={self.price}>"
