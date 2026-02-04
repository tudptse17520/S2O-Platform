from typing import List, Optional
import uuid
from dataclasses import dataclass
from datetime import datetime
from sqlalchemy.orm import Session

from ...domain.interfaces.istaff_profile_repository import IStaffProfileRepository
from ...domain.models.staff_profile import StaffProfile
from ..models.staff_profile_model import StaffProfile as StaffProfileModel


class StaffProfileRepository(IStaffProfileRepository):
    """Repository implementation for StaffProfile entity"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def _to_domain(self, model: StaffProfileModel) -> StaffProfile:
        return StaffProfile(
            id=model.id,
            user_id=model.user_id,
            tenant_id=model.tenant_id,
            branch_id=model.branch_id,
            position=model.position,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
    
    def _to_orm(self, profile: StaffProfile) -> StaffProfileModel:
        model = StaffProfileModel()
        model.id = profile.id if profile.id else uuid.uuid4()
        model.user_id = profile.user_id
        model.tenant_id = profile.tenant_id
        model.branch_id = profile.branch_id
        model.position = profile.position
        return model
    
    def create(self, staff_profile: StaffProfile) -> StaffProfile:
        model = self._to_orm(staff_profile)
        self.db.add(model)
        self.db.flush()
        return self._to_domain(model)
    
    def get_by_user_id(self, user_id: str) -> Optional[StaffProfile]:
        model = self.db.query(StaffProfileModel).filter(
            StaffProfileModel.user_id == uuid.UUID(user_id)
        ).first()
        return self._to_domain(model) if model else None
    
    def get_all(self) -> List[StaffProfile]:
        models = self.db.query(StaffProfileModel).all()
        return [self._to_domain(m) for m in models]
    
    def get_by_tenant(self, tenant_id: str) -> List[StaffProfile]:
        models = self.db.query(StaffProfileModel).filter(
            StaffProfileModel.tenant_id == uuid.UUID(tenant_id)
        ).all()
        return [self._to_domain(m) for m in models]
    
    def get_by_branch(self, branch_id: str) -> List[StaffProfile]:
        models = self.db.query(StaffProfileModel).filter(
            StaffProfileModel.branch_id == uuid.UUID(branch_id)
        ).all()
        return [self._to_domain(m) for m in models]
    
    def get_by_position(self, tenant_id: str, position: str) -> List[StaffProfile]:
        models = self.db.query(StaffProfileModel).filter(
            StaffProfileModel.tenant_id == uuid.UUID(tenant_id),
            StaffProfileModel.position == position
        ).all()
        return [self._to_domain(m) for m in models]
    
    def update(self, user_id: str, staff_profile: StaffProfile) -> StaffProfile:
        model = self.db.query(StaffProfileModel).filter(
            StaffProfileModel.user_id == uuid.UUID(user_id)
        ).first()
        if not model:
            raise ValueError(f"Staff profile for user {user_id} not found")
        
        model.branch_id = staff_profile.branch_id
        model.position = staff_profile.position
        self.db.flush()
        return self._to_domain(model)
    
    def delete(self, user_id: str) -> bool:
        model = self.db.query(StaffProfileModel).filter(
            StaffProfileModel.user_id == uuid.UUID(user_id)
        ).first()
        if model:
            self.db.delete(model)
            return True
        return False
