from abc import ABC, abstractmethod
from typing import List, Optional
from domain.models.tenant import Tenant


class ITenantRepository(ABC):
	"""
	Interface for Tenant Repository
	Defines contract for tenant data access operations.
	"""

	@abstractmethod
	def create(self, tenant: Tenant) -> Tenant:
		"""Create a new tenant"""
		pass

	@abstractmethod
	def get_by_id(self, tenant_id: str) -> Optional[Tenant]:
		"""Get tenant by ID"""
		pass

	@abstractmethod
	def get_all(self) -> List[Tenant]:
		"""Get all tenants"""
		pass

	@abstractmethod
	def get_by_domain(self, domain: str) -> Optional[Tenant]:
		"""Get tenant by domain or unique key"""
		pass

	@abstractmethod
	def update(self, tenant_id: str, tenant: Tenant) -> Tenant:
		"""Update tenant"""
		pass

	@abstractmethod
	def delete(self, tenant_id: str) -> bool:
		"""Delete tenant"""
		pass

