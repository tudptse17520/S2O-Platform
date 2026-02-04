from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID


class CreateTenantRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    subscription_plan: Optional[str] = "FREE"
    is_active: Optional[bool] = True


class UpdateTenantRequest(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    subscription_plan: Optional[str] = None
    is_active: Optional[bool] = None


class TenantResponse(BaseModel):
    id: str
    name: str
    slug: str
    subscription_plan: str
    is_active: bool
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
