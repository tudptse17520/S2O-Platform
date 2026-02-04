from pydantic import BaseModel
from typing import Optional


class CreateStaffProfileRequest(BaseModel):
    branch_id: Optional[str] = None
    position: Optional[str] = None


class UpdateStaffProfileRequest(BaseModel):
    branch_id: Optional[str] = None
    position: Optional[str] = None


class StaffProfileResponse(BaseModel):
    id: str
    user_id: str
    tenant_id: str
    branch_id: Optional[str]
    position: Optional[str]
    created_at: Optional[str]
    updated_at: Optional[str]
