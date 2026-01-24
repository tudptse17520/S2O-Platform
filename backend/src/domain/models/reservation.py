(from typing import Optional)
from datetime import datetime
from enum import Enum


class ReservationStatus(str, Enum):
	PENDING = "PENDING"
	APPROVED = "APPROVED"
	REJECTED = "REJECTED"
	CANCELLED = "CANCELLED"


class Reservation:
	"""
	Domain model for Reservation (table booking).
	Maps to the `reservations` table in DRD.
	"""

	def __init__(
		self,
		id: str,
		tenant_id: str,
		branch_id: str,
		user_id: str,
		booking_time: datetime,
		party_size: int,
		status: str = ReservationStatus.PENDING,
		created_at: Optional[datetime] = None,
	):
		self.id = id
		self.tenant_id = tenant_id
		self.branch_id = branch_id
		self.user_id = user_id
		self.booking_time = booking_time
		self.party_size = party_size
		self.status = status
		self.created_at = created_at or datetime.utcnow()

	def approve(self) -> None:
		self.status = ReservationStatus.APPROVED

	def reject(self) -> None:
		self.status = ReservationStatus.REJECTED

	def cancel(self) -> None:
		self.status = ReservationStatus.CANCELLED

	def is_valid(self) -> bool:
		return bool(self.id and self.tenant_id and self.branch_id and self.user_id and self.party_size > 0)

	def __repr__(self) -> str:
		return f"<Reservation id={self.id} booking_time={self.booking_time} party_size={self.party_size} status={self.status}>"

