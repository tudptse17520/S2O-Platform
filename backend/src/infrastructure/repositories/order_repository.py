from typing import List, Optional
from sqlalchemy.orm import Session
from ...domain.interfaces.iorder_repository import IOrderRepository
from ...domain.models.order import Order as DomainOrder
from ...infrastructure.models import Order as ORMOrder


class OrderRepository(IOrderRepository):
    """SQLAlchemy implementation of IOrderRepository"""
    
    def __init__(self, session: Session):
        self.session = session

    def _to_domain(self, orm_order: ORMOrder) -> DomainOrder:
        """Convert ORM model to domain model"""
        return DomainOrder(
            id=str(orm_order.id),
            tenant_id=str(orm_order.tenant_id),
            branch_id=str(orm_order.branch_id),
            table_id=str(orm_order.table_id) if orm_order.table_id else None,
            customer_id=str(orm_order.customer_id) if orm_order.customer_id else None,
            status=orm_order.status.value if orm_order.status else "PENDING",
            total_amount=orm_order.total_amount or 0.0,
            note=orm_order.note,
            created_at=orm_order.created_at,
            updated_at=orm_order.updated_at
        )

    def _to_orm(self, domain_order: DomainOrder) -> ORMOrder:
        """Convert domain model to ORM model"""
        from ...infrastructure.models import OrderStatus as ORMOrderStatus
        return ORMOrder(
            id=domain_order.id,
            tenant_id=domain_order.tenant_id,
            branch_id=domain_order.branch_id,
            table_id=domain_order.table_id,
            customer_id=domain_order.customer_id,
            status=ORMOrderStatus(domain_order.status) if domain_order.status else ORMOrderStatus.PENDING,
            total_amount=domain_order.total_amount,
            note=domain_order.note,
            created_at=domain_order.created_at,
            updated_at=domain_order.updated_at
        )

    def create(self, order: DomainOrder) -> DomainOrder:
        """Create a new order"""
        orm_order = self._to_orm(order)
        self.session.add(orm_order)
        self.session.flush()
        return order

    def get_by_id(self, order_id: str) -> Optional[DomainOrder]:
        """Get order by ID"""
        orm_order = self.session.query(ORMOrder).filter_by(id=order_id).first()
        if orm_order:
            return self._to_domain(orm_order)
        return None

    def get_all(self) -> List[DomainOrder]:
        """Get all orders"""
        orm_orders = self.session.query(ORMOrder).all()
        return [self._to_domain(o) for o in orm_orders]

    def get_by_tenant(self, tenant_id: str) -> List[DomainOrder]:
        """Get all orders for a tenant"""
        orm_orders = self.session.query(ORMOrder).filter_by(tenant_id=tenant_id).all()
        return [self._to_domain(o) for o in orm_orders]

    def get_by_table(self, table_id: str) -> List[DomainOrder]:
        """Get orders for a table"""
        orm_orders = self.session.query(ORMOrder).filter_by(table_id=table_id).all()
        return [self._to_domain(o) for o in orm_orders]

    def get_by_status(self, tenant_id: str, status: str) -> List[DomainOrder]:
        """Get orders by status for a tenant"""
        from ...infrastructure.models import OrderStatus as ORMOrderStatus
        orm_orders = self.session.query(ORMOrder).filter_by(
            tenant_id=tenant_id, 
            status=ORMOrderStatus(status)
        ).all()
        return [self._to_domain(o) for o in orm_orders]

    def update(self, order_id: str, order: DomainOrder) -> DomainOrder:
        """Update order"""
        from ...infrastructure.models import OrderStatus as ORMOrderStatus
        orm_order = self.session.query(ORMOrder).filter_by(id=order_id).first()
        if orm_order:
            orm_order.status = ORMOrderStatus(order.status) if order.status else orm_order.status
            orm_order.total_amount = order.total_amount
            orm_order.note = order.note
            orm_order.updated_at = order.updated_at
            self.session.flush()
            return self._to_domain(orm_order)
        raise ValueError(f"Order with id {order_id} not found")

    def delete(self, order_id: str) -> bool:
        """Delete order"""
        orm_order = self.session.query(ORMOrder).filter_by(id=order_id).first()
        if orm_order:
            self.session.delete(orm_order)
            self.session.flush()
            return True
        return False
