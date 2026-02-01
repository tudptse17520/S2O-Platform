from abc import ABC, abstractmethod
from typing import List, Optional
from ..models.product import Product


class IMenuRepository(ABC):
	"""
	Interface for Product/Menu Repository
	Defines contract for product/menu data access operations.
	"""

	@abstractmethod
	def create(self, product: Product) -> Product:
		"""Create a new product"""
		pass

	@abstractmethod
	def get_by_id(self, product_id: str) -> Optional[Product]:
		"""Get product by ID"""
		pass

	@abstractmethod
	def get_all(self) -> List[Product]:
		"""Get all products"""
		pass

	@abstractmethod
	def get_by_tenant(self, tenant_id: str) -> List[Product]:
		"""Get all products for a tenant"""
		pass

	@abstractmethod
	def update(self, product_id: str, product: Product) -> Product:
		"""Update product"""
		pass

	@abstractmethod
	def delete(self, product_id: str) -> bool:
		"""Delete product"""
		pass

	@abstractmethod
	def get_by_category(self, tenant_id: str, category_id: str) -> List[Product]:
		"""Get products by category for a tenant"""
		pass

	@abstractmethod
	def search(self, tenant_id: str, query: str) -> List[Product]:
		"""Search products by text query"""
		pass

