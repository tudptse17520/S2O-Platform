from typing import Optional
from sqlalchemy.orm import Session
from ...domain.interfaces.itenant_repository import ITenantRepository
from ...domain.models.tenant import Tenant as DomainTenant
from ...domain.models.staff_profile import StaffProfile as DomainStaffProfile
from ...infrastructure.models import Tenant as ORMTenant
from ...infrastructure.models import StaffProfile as ORMStaffProfile

class SQLTenantRepository(ITenantRepository):
    def __init__(self, session: Session):
        self.session = session

    def save(self, tenant: DomainTenant) -> DomainTenant:
        orm_tenant = ORMTenant(
            id=tenant.id,
            name=tenant.name,
            slug=tenant.slug,
            subscription_plan=tenant.subscription_plan,
            is_active=tenant.is_active,
            created_at=tenant.created_at,
            updated_at=tenant.updated_at
        )
        self.session.add(orm_tenant)
        self.session.flush()
        return tenant

    def save_staff_profile(self, profile: DomainStaffProfile) -> DomainStaffProfile:
        orm_profile = ORMStaffProfile(
            id=profile.id,
            user_id=profile.user_id,
            tenant_id=profile.tenant_id,
            branch_id=profile.branch_id,
            position=profile.position,
            created_at=profile.created_at,
            updated_at=profile.updated_at
        )
        self.session.add(orm_profile)
        self.session.flush()
        return profile
    
    def get_staff_profile_by_user_id(self, user_id: str) -> Optional[DomainStaffProfile]:
        orm_profile = self.session.query(ORMStaffProfile).filter_by(user_id=user_id).first()
        if orm_profile:
            return DomainStaffProfile(
                id=orm_profile.id,
                user_id=orm_profile.user_id,
                tenant_id=orm_profile.tenant_id,
                branch_id=orm_profile.branch_id,
                position=orm_profile.position,
                created_at=orm_profile.created_at,
                updated_at=orm_profile.updated_at
            )
        return None
