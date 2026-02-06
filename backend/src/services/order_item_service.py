from typing import List, Optional, Dict, Any
import uuid

from ..domain.interfaces.iorder_item_repository import IOrderItemRepository
from ..domain.models.order_item import OrderItem


class OrderItemService:
    """Service for order item business logic"""
    
    def __init__(self, order_item_repo: IOrderItemRepository):
        self.order_item_repo = order_item_repo
    
    def create_order_item(self, tenant_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new order item"""
        order_item = OrderItem(
            id=str(uuid.uuid4()),
            tenant_id=tenant_id,
            order_id=data['order_id'],
            product_id=data['product_id'],
            quantity=data['quantity'],
            price_at_order=data['price_at_order'],
            item_status=data.get('item_status', 'PENDING')
        )
        
        created = self.order_item_repo.create(order_item)
        return self._to_dict(created)
    
    def get_order_item(self, order_item_id: str) -> Optional[Dict[str, Any]]:
        """Get order item by ID"""
        order_item = self.order_item_repo.get_by_id(order_item_id)
        return self._to_dict(order_item) if order_item else None
    
    def get_order_items_by_order(self, order_id: str) -> List[Dict[str, Any]]:
        """Get all items for an order"""
        items = self.order_item_repo.get_by_order(order_id)
        return [self._to_dict(i) for i in items]
    
    def get_order_items_by_status(self, order_id: str, status: str) -> List[Dict[str, Any]]:
        """Get items by status for an order"""
        items = self.order_item_repo.get_by_status(order_id, status)
        return [self._to_dict(i) for i in items]
    
    def update_order_item(self, order_item_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update order item"""
        order_item = self.order_item_repo.get_by_id(order_item_id)
        if not order_item:
            raise ValueError(f"Order item {order_item_id} not found")
        
        if 'quantity' in data and data['quantity'] is not None:
            order_item.quantity = data['quantity']
        if 'item_status' in data and data['item_status'] is not None:
            order_item.item_status = data['item_status']
        
        updated = self.order_item_repo.update(order_item_id, order_item)
        return self._to_dict(updated)
    
    def update_status(self, order_item_id: str, status: str) -> Dict[str, Any]:
        """Update order item status"""
        order_item = self.order_item_repo.get_by_id(order_item_id)
        if not order_item:
            raise ValueError(f"Order item {order_item_id} not found")
        
        order_item.item_status = status
        updated = self.order_item_repo.update(order_item_id, order_item)
        return self._to_dict(updated)
    
    def mark_cooking(self, order_item_id: str) -> Dict[str, Any]:
        """Mark order item as cooking"""
        return self.update_status(order_item_id, "COOKING")
    
    def mark_ready(self, order_item_id: str) -> Dict[str, Any]:
        """Mark order item as ready"""
        return self.update_status(order_item_id, "READY")
    
    def mark_served(self, order_item_id: str) -> Dict[str, Any]:
        """Mark order item as served"""
        return self.update_status(order_item_id, "SERVED")
    
    def cancel_order_item(self, order_item_id: str) -> Dict[str, Any]:
        """Cancel order item"""
        return self.update_status(order_item_id, "CANCELLED")
    
    def delete_order_item(self, order_item_id: str) -> bool:
        """Delete order item"""
        return self.order_item_repo.delete(order_item_id)
    
    def _to_dict(self, order_item: OrderItem) -> Dict[str, Any]:
        return {
            "id": str(order_item.id),
            "tenant_id": str(order_item.tenant_id),
            "order_id": str(order_item.order_id),
            "product_id": str(order_item.product_id),
            "quantity": order_item.quantity,
            "price_at_order": order_item.price_at_order,
            "item_status": order_item.item_status,
            "subtotal": order_item.get_subtotal()
        }
