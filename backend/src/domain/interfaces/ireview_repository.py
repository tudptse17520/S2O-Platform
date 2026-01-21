from abc import ABC, abstractmethod
from typing import List, Optional
from domain.models.review import Review


class IReviewRepository(ABC):
	"""
	Interface for Review Repository
	Defines contract for review data access operations.
	"""

	@abstractmethod
	def create(self, review: Review) -> Review:
		"""Create a new review"""
		pass

	@abstractmethod
	def get_by_id(self, review_id: str) -> Optional[Review]:
		"""Get review by ID"""
		pass

	@abstractmethod
	def get_all(self) -> List[Review]:
		"""Get all reviews"""
		pass

	@abstractmethod
	def get_by_tenant(self, tenant_id: str) -> List[Review]:
		"""Get all reviews for a tenant"""
		pass

	@abstractmethod
	def get_by_product(self, product_id: str) -> List[Review]:
		"""Get reviews for a product"""
		pass

	@abstractmethod
	def get_by_user(self, user_id: str) -> List[Review]:
		"""Get reviews written by a user"""
		pass

	@abstractmethod
	def update(self, review_id: str, review: Review) -> Review:
		"""Update review"""
		pass

	@abstractmethod
	def delete(self, review_id: str) -> bool:
		"""Delete review"""
		pass

