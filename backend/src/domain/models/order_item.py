from typing import Optional
from enum import Enum


class OrderItemStatus(str, Enum):
    """Enum for order item statuses"""
    PENDING = "PENDING"
    COOKING = "COOKING"
    READY = "READY"
    SERVED = "SERVED"
    CANCELLED = "CANCELLED"


class OrderItem:
    """
    Domain Model for Order Item
    
    Represents a single item in an order.
    Attributes map to the 'order_items' table in DRD.
    """
    
    def __init__(
        self,
        id: str,
        tenant_id: str,
        order_id: str,
        product_id: str,
        quantity: int,
        price_at_order: float,
        item_status: str = OrderItemStatus.PENDING
    ):
        self.id = id
        self.tenant_id = tenant_id
        self.order_id = order_id
        self.product_id = product_id
        self.quantity = quantity
        self.price_at_order = price_at_order
        self.item_status = item_status
    
    def mark_cooking(self) -> None:
        """Mark item as being cooked"""
        self.item_status = OrderItemStatus.COOKING
    
    def mark_ready(self) -> None:
        """Mark item as ready to serve"""
        self.item_status = OrderItemStatus.READY
    
    def mark_served(self) -> None:
        """Mark item as served to customer"""
        self.item_status = OrderItemStatus.SERVED
    
    def cancel(self) -> None:
        """Cancel this order item"""
        self.item_status = OrderItemStatus.CANCELLED
    
    def get_subtotal(self) -> float:
        """Calculate subtotal (price * quantity)"""
        return self.price_at_order * self.quantity
    
    def is_valid(self) -> bool:
        """Validate order item data"""
        return (
            self.quantity > 0 
            and self.price_at_order > 0 
            and self.order_id 
            and self.product_id 
            and self.tenant_id
        )
    
    def __repr__(self) -> str:
        return f"<OrderItem id={self.id} product_id={self.product_id} qty={self.quantity} status={self.item_status}>"
