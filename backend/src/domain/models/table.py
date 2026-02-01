from typing import Optional
from enum import Enum
from datetime import datetime


class TableStatus(str, Enum):
	AVAILABLE = "AVAILABLE"
	OCCUPIED = "OCCUPIED"
	RESERVED = "RESERVED"


class Table:
	"""
	Domain model for physical table in a branch.
	Maps to the `tables` table in the DRD.
	"""

	def __init__(
		self,
		id: str,
		tenant_id: str,
		branch_id: str,
		name: str,
		qr_code_link: Optional[str] = None,
		status: str = TableStatus.AVAILABLE,
		created_at: Optional[datetime] = None,
		updated_at: Optional[datetime] = None,
	):
		self.id = id
		self.tenant_id = tenant_id
		self.branch_id = branch_id
		self.name = name
		self.qr_code_link = qr_code_link
		self.status = status
		self.created_at = created_at or datetime.utcnow()
		self.updated_at = updated_at or datetime.utcnow()

	def set_status(self, new_status: str) -> None:
		self.status = new_status
		self.updated_at = datetime.utcnow()

	def is_available(self) -> bool:
		return self.status == TableStatus.AVAILABLE

	def is_valid(self) -> bool:
		return bool(self.id and self.tenant_id and self.branch_id and self.name)

	def __repr__(self) -> str:
		return f"<Table id={self.id} name={self.name} status={self.status}>"
