import uuid
from enum import Enum as PyEnum
from sqlalchemy import String, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from ..databases.base import Base, UUIDMixin, TimestampMixin

class TableStatus(PyEnum):
    AVAILABLE = "AVAILABLE"
    OCCUPIED = "OCCUPIED"

class Table(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "tables"

    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("tenants.id"), nullable=False)
    branch_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("branches.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    status: Mapped[TableStatus] = mapped_column(Enum(TableStatus), default=TableStatus.AVAILABLE)
