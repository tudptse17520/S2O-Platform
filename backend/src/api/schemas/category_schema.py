from pydantic import BaseModel, Field
from typing import Optional


class CreateCategoryRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    display_order: int = Field(default=0, ge=0)


class UpdateCategoryRequest(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    display_order: Optional[int] = Field(None, ge=0)


class CategoryResponse(BaseModel):
    id: str
    tenant_id: str
    name: str
    display_order: int
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
