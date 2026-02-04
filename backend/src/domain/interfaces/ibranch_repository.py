from abc import ABC, abstractmethod
from typing import List, Optional
from ..models.branch import Branch


class IBranchRepository(ABC):
	"""
	Interface for Branch Repository
	Defines contract for branch data access operations.
	"""

	@abstractmethod
	def create(self, branch: Branch) -> Branch:
		"""Create a new branch"""
		pass

	@abstractmethod
	def get_by_id(self, branch_id: str) -> Optional[Branch]:
		"""Get branch by ID"""
		pass

	@abstractmethod
	def get_all(self) -> List[Branch]:
		"""Get all branches"""
		pass

	@abstractmethod
	def get_by_tenant(self, tenant_id: str) -> List[Branch]:
		"""Get all branches for a tenant"""
		pass

	@abstractmethod
	def update(self, branch_id: str, branch: Branch) -> Branch:
		"""Update branch"""
		pass

	@abstractmethod
	def delete(self, branch_id: str) -> bool:
		"""Delete branch"""
		pass

	@abstractmethod
	def get_by_name(self, tenant_id: str, name: str) -> Optional[Branch]:
		"""Find branch by name within a tenant"""
		pass

