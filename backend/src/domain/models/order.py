(from typing import Optional, List)
from datetime import datetime
from enum import Enum


class OrderStatus(str, Enum):
	PENDING = "PENDING"
	CONFIRMED = "CONFIRMED"
	COOKING = "COOKING"
	SERVED = "SERVED"
	COMPLETED = "COMPLETED"
	CANCELLED = "CANCELLED"


class Order:
	"""
	Domain model for Order.
	Maps to the `orders` table in DRD.
	"""

	def __init__(
		self,
		id: str,
		tenant_id: str,
		branch_id: str,
		table_id: Optional[str],
		customer_id: Optional[str],
		status: str = OrderStatus.PENDING,
		total_amount: float = 0.0,
		note: Optional[str] = None,
		created_at: Optional[datetime] = None,
		updated_at: Optional[datetime] = None,
	):
		self.id = id
		self.tenant_id = tenant_id
		self.branch_id = branch_id
		self.table_id = table_id
		self.customer_id = customer_id
		self.status = status
		self.total_amount = total_amount
		self.note = note
		self.created_at = created_at or datetime.utcnow()
		self.updated_at = updated_at or datetime.utcnow()
		self.items: List = []

	def add_item(self, item) -> None:
		self.items.append(item)
		self.total_amount += getattr(item, 'get_subtotal', lambda: 0)()
		self.updated_at = datetime.utcnow()

	def update_status(self, new_status: str) -> None:
		self.status = new_status
		self.updated_at = datetime.utcnow()

	def is_valid(self) -> bool:
		return bool(self.id and self.tenant_id and self.branch_id)

	def __repr__(self) -> str:
		return f"<Order id={self.id} status={self.status} total={self.total_amount}>"

