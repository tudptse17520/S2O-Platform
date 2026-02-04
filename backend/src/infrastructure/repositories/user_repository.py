from typing import Optional, List
import uuid
from sqlalchemy.orm import Session
from ...domain.interfaces.iuser_repository import IUserRepository
from ...domain.models.user import User as DomainUser, UserRole
from ...infrastructure.models import User as ORMUser
from ...infrastructure.models import StaffProfile as ORMStaffProfile


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

    def get_by_id(self, user_id: str) -> Optional[DomainUser]:
        orm_user = self.session.query(ORMUser).filter(
            ORMUser.id == uuid.UUID(user_id)
        ).first()
        if orm_user:
            return self._to_domain(orm_user)
        return None

    def get_all(self) -> List[DomainUser]:
        orm_users = self.session.query(ORMUser).all()
        return [self._to_domain(u) for u in orm_users]

    def get_by_tenant(self, tenant_id: str) -> List[DomainUser]:
        """Get users by tenant via staff_profile association"""
        # Join users with staff_profiles to get users by tenant
        tid = uuid.UUID(tenant_id)
        staff_profiles = self.session.query(ORMStaffProfile).filter(
            ORMStaffProfile.tenant_id == tid
        ).all()
        user_ids = [sp.user_id for sp in staff_profiles]
        
        if not user_ids:
            return []
        
        orm_users = self.session.query(ORMUser).filter(
            ORMUser.id.in_(user_ids)
        ).all()
        return [self._to_domain(u) for u in orm_users]

    def save(self, user: DomainUser, tenant_id: str = None) -> DomainUser:
        orm_user = ORMUser(
            id=user.id,
            email=user.email,
            password_hash=user.password_hash,
            full_name=user.full_name,
            role=user.role,
            created_at=user.created_at,
            updated_at=user.updated_at
        )
        self.session.add(orm_user)
        self.session.flush()
        return user

    def update(self, user_id: str, user: DomainUser) -> DomainUser:
        orm_user = self.session.query(ORMUser).filter(
            ORMUser.id == uuid.UUID(user_id)
        ).first()
        if not orm_user:
            raise ValueError(f"User {user_id} not found")
        
        orm_user.full_name = user.full_name
        orm_user.role = user.role
        self.session.flush()
        return self._to_domain(orm_user)

    def delete(self, user_id: str) -> bool:
        orm_user = self.session.query(ORMUser).filter(
            ORMUser.id == uuid.UUID(user_id)
        ).first()
        if orm_user:
            self.session.delete(orm_user)
            return True
        return False
