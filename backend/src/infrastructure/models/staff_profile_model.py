import uuid
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from ..databases.base import Base, UUIDMixin, TimestampMixin

class StaffProfile(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "staff_profiles"

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("tenants.id"), nullable=False)
    branch_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("branches.id"), nullable=True)
    position: Mapped[str] = mapped_column(String(100), nullable=True)
