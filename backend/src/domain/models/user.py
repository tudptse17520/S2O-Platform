(from typing import Optional)
from datetime import datetime


class User:
	"""
	Domain model for User (central identity table).
	Maps to the `users` table in the DRD.
	"""

	def __init__(
		self,
		id: str,
		email: str,
		password_hash: Optional[str] = None,
		role: str = "CUSTOMER",
		full_name: Optional[str] = None,
		avatar_url: Optional[str] = None,
		created_at: Optional[datetime] = None,
		updated_at: Optional[datetime] = None,
	):
		self.id = id
		self.email = email
		self.password_hash = password_hash
		self.role = role
		self.full_name = full_name
		self.avatar_url = avatar_url
		self.created_at = created_at or datetime.utcnow()
		self.updated_at = updated_at or datetime.utcnow()

	def set_password_hash(self, password_hash: str) -> None:
		self.password_hash = password_hash

	def is_admin(self) -> bool:
		return self.role.upper() in ("SYS_ADMIN", "OWNER")

	def is_valid(self) -> bool:
		return bool(self.id and self.email)

	def __repr__(self) -> str:
		return f"<User id={self.id} email={self.email} role={self.role}>"

