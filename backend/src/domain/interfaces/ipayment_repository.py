from abc import ABC, abstractmethod
from typing import List, Optional
from domain.models.payment import Payment


class IPaymentRepository(ABC):
	"""
	Interface for Payment Repository
	Defines contract for payment data access operations.
	"""

	@abstractmethod
	def create(self, payment: Payment) -> Payment:
		"""Create a new payment record"""
		pass

	@abstractmethod
	def get_by_id(self, payment_id: str) -> Optional[Payment]:
		"""Get payment by ID"""
		pass

	@abstractmethod
	def get_all(self) -> List[Payment]:
		"""Get all payments"""
		pass

	@abstractmethod
	def get_by_order(self, order_id: str) -> List[Payment]:
		"""Get payments for an order"""
		pass

	@abstractmethod
	def get_by_tenant(self, tenant_id: str) -> List[Payment]:
		"""Get payments for a tenant"""
		pass

	@abstractmethod
	def refund(self, payment_id: str, amount: float) -> Payment:
		"""Issue a refund against a payment"""
		pass

	@abstractmethod
	def update(self, payment_id: str, payment: Payment) -> Payment:
		"""Update payment record"""
		pass

