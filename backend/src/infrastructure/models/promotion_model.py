import uuid
from sqlalchemy import String, Float, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from ..databases.base import Base, UUIDMixin, TimestampMixin

class Promotion(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "promotions"

    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("tenants.id"), nullable=False)
    code: Mapped[str] = mapped_column(String(50), nullable=False)
    type: Mapped[str] = mapped_column(String(20), nullable=False) # e.g., 'PERCENTAGE', 'FIXED_AMOUNT'
    value: Mapped[float] = mapped_column(Float, nullable=False)
    start_date: Mapped[DateTime] = mapped_column(DateTime, nullable=True)
    end_date: Mapped[DateTime] = mapped_column(DateTime, nullable=True)

class PromotionProduct(Base):
    __tablename__ = "promotion_products"
    
    promotion_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("promotions.id"), primary_key=True)
    product_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("products.id"), primary_key=True)
