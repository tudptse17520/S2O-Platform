from abc import ABC, abstractmethod
from typing import List, Optional
from ..models.table import Table


class ITableRepository(ABC):
	"""
	Interface for Table Repository
	Defines contract for table data access operations.
	"""

	@abstractmethod
	def create(self, table: Table) -> Table:
		"""Create a new table"""
		pass

	@abstractmethod
	def get_by_id(self, table_id: str) -> Optional[Table]:
		"""Get table by ID"""
		pass

	@abstractmethod
	def get_all(self) -> List[Table]:
		"""Get all tables"""
		pass

	@abstractmethod
	def get_by_tenant(self, tenant_id: str) -> List[Table]:
		"""Get all tables for a tenant"""
		pass

	@abstractmethod
	def get_by_status(self, tenant_id: str, status: str) -> List[Table]:
		"""Get tables by status (available/occupied)"""
		pass

	@abstractmethod
	def find_available(self, tenant_id: str, seats: int) -> List[Table]:
		"""Find available tables that match seat count"""
		pass

	@abstractmethod
	def update(self, table_id: str, table: Table) -> Table:
		"""Update table"""
		pass

	@abstractmethod
	def delete(self, table_id: str) -> bool:
		"""Delete table"""
		pass

