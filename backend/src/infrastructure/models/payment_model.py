import uuid
from enum import Enum as PyEnum
from sqlalchemy import Float, Enum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column
from ..databases.base import Base, UUIDMixin, TimestampMixin


class PaymentMethodEnum(PyEnum):
    CASH = "CASH"
    CARD = "CARD"
    VIETQR = "VIETQR"
    BANK_TRANSFER = "BANK_TRANSFER"


class PaymentStatusEnum(PyEnum):
    PENDING = "PENDING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    REFUNDED = "REFUNDED"


class Payment(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "payments"

    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("tenants.id"), nullable=False)
    order_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("orders.id"), nullable=True)
    
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    method: Mapped[str] = mapped_column(String(50), nullable=False, default="VIETQR")
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="PENDING")
    transaction_id: Mapped[str] = mapped_column(String(100), nullable=True)
