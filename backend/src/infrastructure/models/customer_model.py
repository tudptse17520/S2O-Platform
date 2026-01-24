import uuid
from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from ..base import Base, UUIDMixin, TimestampMixin

class Customer(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "customers"

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("tenants.id"), nullable=False)
    phone_number: Mapped[str] = mapped_column(String(20), nullable=True)
    loyalty_points: Mapped[int] = mapped_column(Integer, default=0)
