from abc import ABC, abstractmethod
from typing import List, Optional
from ..models.order import Order


class IOrderRepository(ABC):
	"""
	Interface for Order Repository
	Defines contract for order data access operations.
	"""

	@abstractmethod
	def create(self, order: Order) -> Order:
		"""Create a new order"""
		pass

	@abstractmethod
	def get_by_id(self, order_id: str) -> Optional[Order]:
		"""Get order by ID"""
		pass

	@abstractmethod
	def get_all(self) -> List[Order]:
		"""Get all orders"""
		pass

	@abstractmethod
	def get_by_tenant(self, tenant_id: str) -> List[Order]:
		"""Get all orders for a tenant"""
		pass

	@abstractmethod
	def get_by_table(self, table_id: str) -> List[Order]:
		"""Get orders for a table"""
		pass

	@abstractmethod
	def get_by_status(self, tenant_id: str, status: str) -> List[Order]:
		"""Get orders by status for a tenant"""
		pass

	@abstractmethod
	def update(self, order_id: str, order: Order) -> Order:
		"""Update order"""
		pass

	@abstractmethod
	def delete(self, order_id: str) -> bool:
		"""Delete order"""
		pass

