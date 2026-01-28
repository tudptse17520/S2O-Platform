from typing import Optional
from sqlalchemy.orm import Session
from ...domain.interfaces.iuser_repository import IUserRepository
from ...domain.models.user import User as DomainUser, UserRole
from ...infrastructure.models import User as ORMUser

class UserRepository(IUserRepository):
    def __init__(self, session: Session):
        self.session = session

    def _to_domain(self, orm_user: ORMUser) -> DomainUser:
        return DomainUser(
            id=orm_user.id,
            email=orm_user.email,
            password_hash=orm_user.password_hash,
            full_name=orm_user.full_name,
            role=UserRole(orm_user.role.value),
            created_at=orm_user.created_at,
            updated_at=orm_user.updated_at
        )

    def get_by_email(self, email: str) -> Optional[DomainUser]:
        orm_user = self.session.query(ORMUser).filter_by(email=email).first()
        if orm_user:
            return self._to_domain(orm_user)
        return None

    def save(self, user: DomainUser) -> DomainUser:
        # Check if exists (for update) or new (for insert)
        # For simplicity, we assume we are creating a new one if not in session, 
        # but pure DDD usually tracks identity. 
        # Here we just map domain -> ORM for creation.
        
        orm_user = ORMUser(
            id=user.id,
            email=user.email,
            password_hash=user.password_hash,
            full_name=user.full_name,
            role=user.role, # Enum should match if we are careful
            created_at=user.created_at,
            updated_at=user.updated_at
        )
        self.session.add(orm_user)
        self.session.flush() # To ensure ID collision checks etc.
        return user
