import uuid
from enum import Enum as PyEnum
from sqlalchemy import Integer, Float, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from ..base import Base, UUIDMixin, TimestampMixin

class OrderItemStatus(PyEnum):
    PENDING = "PENDING"
    PREPARING = "PREPARING"
    SERVED = "SERVED"
    CANCELLED = "CANCELLED"

class OrderItem(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "order_items"

    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("tenants.id"), nullable=False)
    order_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("orders.id"), nullable=False)
    product_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("products.id"), nullable=False)
    
    quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    price_at_order: Mapped[float] = mapped_column(Float, nullable=False)
    item_status: Mapped[OrderItemStatus] = mapped_column(Enum(OrderItemStatus), default=OrderItemStatus.PENDING)
