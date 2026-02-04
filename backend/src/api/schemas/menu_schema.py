from pydantic import BaseModel, Field
from typing import Optional, List
from uuid import UUID
from datetime import datetime

class CreateCategoryRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    display_order: int = 0

class CategoryResponse(BaseModel):
    id: UUID
    tenant_id: UUID
    name: str
    display_order: int
    created_at: datetime
    updated_at: datetime

class CreateProductRequest(BaseModel):
    category_id: UUID
    name: str = Field(..., min_length=1, max_length=255)
    price: float = Field(..., gt=0)
    description: Optional[str] = None
    is_available: bool = True

class ProductResponse(BaseModel):
    id: UUID
    tenant_id: UUID
    category_id: UUID
    name: str
    price: float
    description: Optional[str]
    is_available: bool
    created_at: datetime
    updated_at: datetime
