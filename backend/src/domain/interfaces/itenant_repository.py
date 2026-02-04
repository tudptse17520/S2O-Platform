from abc import ABC, abstractmethod
from typing import Optional
from ..models.tenant import Tenant
from ..models.staff_profile import StaffProfile

class ITenantRepository(ABC):
    @abstractmethod
    def save(self, tenant: Tenant) -> Tenant:
        pass

    @abstractmethod
    def save_staff_profile(self, profile: StaffProfile) -> StaffProfile:
        pass
    
    @abstractmethod
    def get_staff_profile_by_user_id(self, user_id: str) -> Optional[StaffProfile]:
        pass
