from abc import ABC, abstractmethod
from typing import List, Optional
from domain.models.order_item import OrderItem


class IOrderItemRepository(ABC):
    """
    Interface for Order Item Repository
    
    Defines contract for order item data access operations.
    """
    
    @abstractmethod
    def create(self, order_item: OrderItem) -> OrderItem:
        """Create a new order item"""
        pass
    
    @abstractmethod
    def get_by_id(self, order_item_id: str) -> Optional[OrderItem]:
        """Get order item by ID"""
        pass
    
    @abstractmethod
    def get_all(self) -> List[OrderItem]:
        """Get all order items"""
        pass
    
    @abstractmethod
    def get_by_order(self, order_id: str) -> List[OrderItem]:
        """Get all items for an order"""
        pass
    
    @abstractmethod
    def get_by_product(self, product_id: str) -> List[OrderItem]:
        """Get all order items for a product"""
        pass
    
    @abstractmethod
    def update(self, order_item_id: str, order_item: OrderItem) -> OrderItem:
        """Update order item"""
        pass
    
    @abstractmethod
    def delete(self, order_item_id: str) -> bool:
        """Delete order item"""
        pass
    
    @abstractmethod
    def get_by_status(self, order_id: str, status: str) -> List[OrderItem]:
        """Get order items by status for an order"""
        pass
