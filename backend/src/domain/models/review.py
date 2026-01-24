(from typing import Optional)
from datetime import datetime


class Review:
	"""
	Domain model for Review (customer rating/comment for an order/restaurant).
	Maps to the `reviews` table in DRD.
	"""

	def __init__(
		self,
		id: str,
		user_id: str,
		tenant_id: str,
		order_id: Optional[str],
		rating: int,
		comment: Optional[str] = None,
		created_at: Optional[datetime] = None,
	):
		self.id = id
		self.user_id = user_id
		self.tenant_id = tenant_id
		self.order_id = order_id
		self.rating = rating
		self.comment = comment
		self.created_at = created_at or datetime.utcnow()

	def is_valid(self) -> bool:
		return bool(self.id and self.user_id and 0 <= self.rating <= 5)

	def __repr__(self) -> str:
		return f"<Review id={self.id} user_id={self.user_id} rating={self.rating}>"

