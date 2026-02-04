from typing import List, Optional, Dict, Any
import uuid
from datetime import datetime

from ..domain.interfaces.istaff_profile_repository import IStaffProfileRepository
from ..domain.models.staff_profile import StaffProfile


class StaffProfileService:
    """Service for staff profile-related business logic"""
    
    def __init__(self, staff_repo: IStaffProfileRepository):
        self.staff_repo = staff_repo
    
    def create_staff_profile(self, user_id: str, tenant_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new staff profile"""
        profile = StaffProfile(
            id=uuid.uuid4(),
            user_id=uuid.UUID(user_id),
            tenant_id=uuid.UUID(tenant_id),
            branch_id=uuid.UUID(data['branch_id']) if data.get('branch_id') else None,
            position=data.get('position'),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        
        created = self.staff_repo.create(profile)
        return self._to_dict(created)
    
    def get_staff_profile(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get staff profile by user ID"""
        profile = self.staff_repo.get_by_user_id(user_id)
        return self._to_dict(profile) if profile else None
    
    def get_staff_by_tenant(self, tenant_id: str) -> List[Dict[str, Any]]:
        """Get all staff for a tenant"""
        profiles = self.staff_repo.get_by_tenant(tenant_id)
        return [self._to_dict(p) for p in profiles]
    
    def get_staff_by_branch(self, branch_id: str) -> List[Dict[str, Any]]:
        """Get all staff for a branch"""
        profiles = self.staff_repo.get_by_branch(branch_id)
        return [self._to_dict(p) for p in profiles]
    
    def get_staff_by_position(self, tenant_id: str, position: str) -> List[Dict[str, Any]]:
        """Get staff by position"""
        profiles = self.staff_repo.get_by_position(tenant_id, position)
        return [self._to_dict(p) for p in profiles]
    
    def update_staff_profile(self, user_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update staff profile"""
        profile = self.staff_repo.get_by_user_id(user_id)
        if not profile:
            raise ValueError(f"Staff profile not found for user {user_id}")
        
        if 'branch_id' in data:
            profile.branch_id = uuid.UUID(data['branch_id']) if data['branch_id'] else None
        if 'position' in data:
            profile.position = data['position']
        
        updated = self.staff_repo.update(user_id, profile)
        return self._to_dict(updated)
    
    def delete_staff_profile(self, user_id: str) -> bool:
        """Delete staff profile"""
        return self.staff_repo.delete(user_id)
    
    def _to_dict(self, profile: StaffProfile) -> Dict[str, Any]:
        return {
            "id": str(profile.id),
            "user_id": str(profile.user_id),
            "tenant_id": str(profile.tenant_id),
            "branch_id": str(profile.branch_id) if profile.branch_id else None,
            "position": profile.position,
            "created_at": profile.created_at.isoformat() if profile.created_at else None,
            "updated_at": profile.updated_at.isoformat() if profile.updated_at else None,
        }
