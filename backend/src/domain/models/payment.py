(from typing import Optional)
from datetime import datetime
from enum import Enum


class PaymentStatus(str, Enum):
	PENDING = "PENDING"
	SUCCESS = "SUCCESS"
	FAILED = "FAILED"
	REFUNDED = "REFUNDED"


class PaymentMethod(str, Enum):
	CASH = "CASH"
	CARD = "CARD"
	VIETQR = "VIETQR"
	BANK_TRANSFER = "BANK_TRANSFER"


class Payment:
	"""
	Domain model for Payment records.
	Maps to a `payments` table.
	"""

	def __init__(
		self,
		id: str,
		tenant_id: str,
		order_id: Optional[str],
		invoice_id: Optional[str],
		amount: float,
		method: str = PaymentMethod.VIETQR,
		status: str = PaymentStatus.PENDING,
		created_at: Optional[datetime] = None,
		updated_at: Optional[datetime] = None,
	):
		self.id = id
		self.tenant_id = tenant_id
		self.order_id = order_id
		self.invoice_id = invoice_id
		self.amount = amount
		self.method = method
		self.status = status
		self.created_at = created_at or datetime.utcnow()
		self.updated_at = updated_at or datetime.utcnow()

	def mark_success(self) -> None:
		self.status = PaymentStatus.SUCCESS
		self.updated_at = datetime.utcnow()

	def mark_failed(self) -> None:
		self.status = PaymentStatus.FAILED
		self.updated_at = datetime.utcnow()

	def refund(self) -> None:
		self.status = PaymentStatus.REFUNDED
		self.updated_at = datetime.utcnow()

	def is_valid(self) -> bool:
		return bool(self.id and self.tenant_id and self.amount >= 0)

	def __repr__(self) -> str:
		return f"<Payment id={self.id} amount={self.amount} status={self.status}>"

