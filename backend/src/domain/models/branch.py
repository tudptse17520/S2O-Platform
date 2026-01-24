(from typing import Optional)
from datetime import datetime


class Branch:
	"""
	Domain model for Branch (physical restaurant location).
	Maps to the `branches` table in the DRD.
	"""

	def __init__(
		self,
		id: str,
		tenant_id: str,
		name: str,
		address: Optional[str] = None,
		phone: Optional[str] = None,
		is_active: bool = True,
		created_at: Optional[datetime] = None,
		updated_at: Optional[datetime] = None,
	):
		self.id = id
		self.tenant_id = tenant_id
		self.name = name
		self.address = address
		self.phone = phone
		self.is_active = is_active
		self.created_at = created_at or datetime.utcnow()
		self.updated_at = updated_at or datetime.utcnow()

	def activate(self) -> None:
		self.is_active = True

	def deactivate(self) -> None:
		self.is_active = False

	def is_valid(self) -> bool:
		return bool(self.id and self.tenant_id and self.name)

	def __repr__(self) -> str:
		return f"<Branch id={self.id} name={self.name} tenant_id={self.tenant_id}>"

