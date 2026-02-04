from abc import ABC, abstractmethod
from typing import List, Optional
from ..models.reservation import Reservation


class IReservationRepository(ABC):
	"""
	Interface for Reservation Repository
	Defines contract for reservation data access operations.
	"""

	@abstractmethod
	def create(self, reservation: Reservation) -> Reservation:
		"""Create a new reservation"""
		pass

	@abstractmethod
	def get_by_id(self, reservation_id: str) -> Optional[Reservation]:
		"""Get reservation by ID"""
		pass

	@abstractmethod
	def get_all(self) -> List[Reservation]:
		"""Get all reservations"""
		pass

	@abstractmethod
	def get_by_user(self, user_id: str) -> List[Reservation]:
		"""Get reservations by user"""
		pass

	@abstractmethod
	def get_upcoming_for_tenant(self, tenant_id: str) -> List[Reservation]:
		"""Get upcoming reservations for a tenant"""
		pass

	@abstractmethod
	def update(self, reservation_id: str, reservation: Reservation) -> Reservation:
		"""Update reservation"""
		pass

	@abstractmethod
	def cancel(self, reservation_id: str) -> bool:
		"""Cancel a reservation"""
		pass

