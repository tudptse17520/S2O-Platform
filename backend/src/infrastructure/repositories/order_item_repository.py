from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from ...domain.interfaces.iorder_item_repository import IOrderItemRepository
from ...domain.models.order_item import OrderItem as DomainOrderItem
from ...infrastructure.models import OrderItem as ORMOrderItem, OrderItemStatus as ORMOrderItemStatus


class OrderItemRepository(IOrderItemRepository):
    """SQLAlchemy implementation of IOrderItemRepository"""
    
    def __init__(self, session: Session):
        self.session = session

    def _to_domain(self, orm_item: ORMOrderItem) -> DomainOrderItem:
        """Convert ORM model to domain model"""
        return DomainOrderItem(
            id=str(orm_item.id),
            tenant_id=str(orm_item.tenant_id),
            order_id=str(orm_item.order_id),
            product_id=str(orm_item.product_id),
            quantity=orm_item.quantity,
            price_at_order=orm_item.price_at_order,
            item_status=orm_item.item_status.value if orm_item.item_status else "PENDING"
        )

    def _to_orm(self, domain_item: DomainOrderItem) -> ORMOrderItem:
        """Convert domain model to ORM model"""
        # Map domain status to ORM status
        status_map = {
            "PENDING": ORMOrderItemStatus.PENDING,
            "COOKING": ORMOrderItemStatus.PREPARING,
            "PREPARING": ORMOrderItemStatus.PREPARING,
            "READY": ORMOrderItemStatus.SERVED,
            "SERVED": ORMOrderItemStatus.SERVED,
            "CANCELLED": ORMOrderItemStatus.CANCELLED
        }
        return ORMOrderItem(
            id=domain_item.id,
            tenant_id=domain_item.tenant_id,
            order_id=domain_item.order_id,
            product_id=domain_item.product_id,
            quantity=domain_item.quantity,
            price_at_order=domain_item.price_at_order,
            item_status=status_map.get(domain_item.item_status, ORMOrderItemStatus.PENDING),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

    def create(self, order_item: DomainOrderItem) -> DomainOrderItem:
        """Create a new order item"""
        orm_item = self._to_orm(order_item)
        self.session.add(orm_item)
        self.session.flush()
        return order_item

    def get_by_id(self, order_item_id: str) -> Optional[DomainOrderItem]:
        """Get order item by ID"""
        orm = self.session.query(ORMOrderItem).filter_by(id=order_item_id).first()
        if orm:
            return self._to_domain(orm)
        return None

    def get_all(self) -> List[DomainOrderItem]:
        """Get all order items"""
        orm_list = self.session.query(ORMOrderItem).all()
        return [self._to_domain(i) for i in orm_list]

    def get_by_order(self, order_id: str) -> List[DomainOrderItem]:
        """Get all items for an order"""
        orm_list = self.session.query(ORMOrderItem).filter_by(order_id=order_id).all()
        return [self._to_domain(i) for i in orm_list]

    def get_by_product(self, product_id: str) -> List[DomainOrderItem]:
        """Get all order items for a product"""
        orm_list = self.session.query(ORMOrderItem).filter_by(product_id=product_id).all()
        return [self._to_domain(i) for i in orm_list]

    def update(self, order_item_id: str, order_item: DomainOrderItem) -> DomainOrderItem:
        """Update order item"""
        orm = self.session.query(ORMOrderItem).filter_by(id=order_item_id).first()
        if orm:
            # Map domain status to ORM status
            status_map = {
                "PENDING": ORMOrderItemStatus.PENDING,
                "COOKING": ORMOrderItemStatus.PREPARING,
                "PREPARING": ORMOrderItemStatus.PREPARING,
                "READY": ORMOrderItemStatus.SERVED,
                "SERVED": ORMOrderItemStatus.SERVED,
                "CANCELLED": ORMOrderItemStatus.CANCELLED
            }
            orm.quantity = order_item.quantity
            orm.price_at_order = order_item.price_at_order
            orm.item_status = status_map.get(order_item.item_status, orm.item_status)
            orm.updated_at = datetime.utcnow()
            self.session.flush()
            return self._to_domain(orm)
        raise ValueError(f"OrderItem with id {order_item_id} not found")

    def delete(self, order_item_id: str) -> bool:
        """Delete order item"""
        orm = self.session.query(ORMOrderItem).filter_by(id=order_item_id).first()
        if orm:
            self.session.delete(orm)
            self.session.flush()
            return True
        return False

    def get_by_status(self, order_id: str, status: str) -> List[DomainOrderItem]:
        """Get order items by status for an order"""
        status_map = {
            "PENDING": ORMOrderItemStatus.PENDING,
            "COOKING": ORMOrderItemStatus.PREPARING,
            "PREPARING": ORMOrderItemStatus.PREPARING,
            "READY": ORMOrderItemStatus.SERVED,
            "SERVED": ORMOrderItemStatus.SERVED,
            "CANCELLED": ORMOrderItemStatus.CANCELLED
        }
        orm_status = status_map.get(status, ORMOrderItemStatus.PENDING)
        orm_list = self.session.query(ORMOrderItem).filter_by(
            order_id=order_id,
            item_status=orm_status
        ).all()
        return [self._to_domain(i) for i in orm_list]
