(from typing import Optional)
from datetime import datetime


class Tenant:
	"""
	Domain model for Tenant (restaurant / business customer).
	Maps to the `tenants` table in the DRD.
	"""

	def __init__(
		self,
		id: str,
		name: str,
		slug: str,
		subscription_plan: Optional[str] = None,
		is_active: bool = True,
		created_at: Optional[datetime] = None,
		updated_at: Optional[datetime] = None,
	):
		self.id = id
		self.name = name
		self.slug = slug
		self.subscription_plan = subscription_plan
		self.is_active = is_active
		self.created_at = created_at or datetime.utcnow()
		self.updated_at = updated_at or datetime.utcnow()

	def activate(self) -> None:
		self.is_active = True

	def deactivate(self) -> None:
		self.is_active = False

	def is_valid(self) -> bool:
		return bool(self.id and self.name and self.slug)

	def __repr__(self) -> str:
		return f"<Tenant id={self.id} name={self.name} active={self.is_active}>"

