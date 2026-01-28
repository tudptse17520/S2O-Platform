import uuid
from enum import Enum as PyEnum
from sqlalchemy import Float, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from ..databases.base import Base, UUIDMixin, TimestampMixin

class PaymentMethod(PyEnum):
    CASH = "CASH"
    CREDIT_CARD = "CREDIT_CARD"
    QR_CODE = "QR_CODE"
    E_WALLET = "E_WALLET"

class PaymentStatus(PyEnum):
    PENDING = "PENDING"
    PAID = "PAID"
    FAILED = "FAILED"
    REFUNDED = "REFUNDED"

class Invoice(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "invoices"

    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("tenants.id"), nullable=False)
    order_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("orders.id"), nullable=False)
    
    final_amount: Mapped[float] = mapped_column(Float, nullable=False)
    payment_method: Mapped[PaymentMethod] = mapped_column(Enum(PaymentMethod), default=PaymentMethod.CASH)
    payment_status: Mapped[PaymentStatus] = mapped_column(Enum(PaymentStatus), default=PaymentStatus.PENDING)
