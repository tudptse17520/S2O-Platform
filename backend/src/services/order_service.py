import uuid
from datetime import datetime
from typing import List, Optional, Dict, Any

from ..domain.interfaces.iorder_repository import IOrderRepository
from ..domain.interfaces.iorder_item_repository import IOrderItemRepository
from ..domain.models.order import Order, OrderStatus
from ..domain.models.order_item import OrderItem


class OrderService:
    """Service layer for Order operations"""
    
    def __init__(self, order_repo: IOrderRepository, order_item_repo: IOrderItemRepository = None):
        self.order_repo = order_repo
        self.order_item_repo = order_item_repo

    def create_order(self, tenant_id: str, branch_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new order"""
        order_id = uuid.uuid4()
        order = Order(
            id=str(order_id),
            tenant_id=tenant_id,
            branch_id=branch_id,
            table_id=data.get('table_id'),
            customer_id=data.get('customer_id'),
            status=OrderStatus.PENDING,
            total_amount=0.0,
            note=data.get('note'),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        saved_order = self.order_repo.create(order)
        return self._to_dict(saved_order)

    def get_order(self, order_id: str) -> Optional[Dict[str, Any]]:
        """Get an order by ID"""
        order = self.order_repo.get_by_id(order_id)
        if order:
            result = self._to_dict(order)
            # Get order items if repo available
            if self.order_item_repo:
                items = self.order_item_repo.get_by_order(order_id)
                result['items'] = [self._item_to_dict(i) for i in items]
            return result
        return None

    def get_orders_by_tenant(self, tenant_id: str) -> List[Dict[str, Any]]:
        """Get all orders for a tenant"""
        orders = self.order_repo.get_by_tenant(tenant_id)
        return [self._to_dict(o) for o in orders]

    def get_orders_by_table(self, table_id: str) -> List[Dict[str, Any]]:
        """Get orders for a table"""
        orders = self.order_repo.get_by_table(table_id)
        return [self._to_dict(o) for o in orders]

    def get_orders_by_status(self, tenant_id: str, status: str) -> List[Dict[str, Any]]:
        """Get orders by status"""
        orders = self.order_repo.get_by_status(tenant_id, status)
        return [self._to_dict(o) for o in orders]

    def update_order_status(self, order_id: str, status: str) -> Dict[str, Any]:
        """Update order status"""
        order = self.order_repo.get_by_id(order_id)
        if not order:
            raise ValueError(f"Order with id {order_id} not found")
        
        order.status = status
        order.updated_at = datetime.utcnow()
        
        updated_order = self.order_repo.update(order_id, order)
        return self._to_dict(updated_order)

    def add_item_to_order(self, order_id: str, tenant_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Add an item to an order"""
        if not self.order_item_repo:
            raise ValueError("Order item repository not available")
        
        order = self.order_repo.get_by_id(order_id)
        if not order:
            raise ValueError(f"Order with id {order_id} not found")
        
        item_id = uuid.uuid4()
        item = OrderItem(
            id=str(item_id),
            tenant_id=tenant_id,
            order_id=order_id,
            product_id=data['product_id'],
            quantity=data.get('quantity', 1),
            price_at_order=data['price']
        )
        
        saved_item = self.order_item_repo.create(item)
        
        # Update order total
        order.total_amount += item.get_subtotal()
        order.updated_at = datetime.utcnow()
        self.order_repo.update(order_id, order)
        
        return self._item_to_dict(saved_item)

    def delete_order(self, order_id: str) -> bool:
        """Delete an order"""
        return self.order_repo.delete(order_id)

    def _to_dict(self, order: Order) -> Dict[str, Any]:
        """Convert order entity to dictionary"""
        return {
            "id": str(order.id),
            "tenant_id": str(order.tenant_id),
            "branch_id": str(order.branch_id),
            "table_id": str(order.table_id) if order.table_id else None,
            "customer_id": str(order.customer_id) if order.customer_id else None,
            "status": order.status if isinstance(order.status, str) else order.status.value,
            "total_amount": order.total_amount,
            "note": order.note,
            "created_at": order.created_at.isoformat() if order.created_at else None,
            "updated_at": order.updated_at.isoformat() if order.updated_at else None
        }

    def _item_to_dict(self, item: OrderItem) -> Dict[str, Any]:
        """Convert order item to dictionary"""
        return {
            "id": str(item.id),
            "order_id": str(item.order_id),
            "product_id": str(item.product_id),
            "quantity": item.quantity,
            "price_at_order": item.price_at_order,
            "subtotal": item.get_subtotal(),
            "item_status": item.item_status if isinstance(item.item_status, str) else item.item_status.value
        }
