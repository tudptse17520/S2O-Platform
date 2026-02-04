from pydantic import BaseModel, Field
from typing import Optional


class CreateBranchRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    address: Optional[str] = Field(None, max_length=500)
    is_active: Optional[bool] = True


class UpdateBranchRequest(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    address: Optional[str] = Field(None, max_length=500)
    is_active: Optional[bool] = None


class BranchResponse(BaseModel):
    id: str
    tenant_id: str
    name: str
    address: Optional[str] = None
    is_active: bool
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
