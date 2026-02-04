from pydantic import BaseModel, Field
from typing import Optional


class CreateReviewRequest(BaseModel):
    order_id: Optional[str] = None
    rating: int = Field(..., ge=1, le=5)
    comment: Optional[str] = None


class UpdateReviewRequest(BaseModel):
    rating: Optional[int] = Field(None, ge=1, le=5)
    comment: Optional[str] = None


class ReviewResponse(BaseModel):
    id: str
    user_id: str
    tenant_id: str
    order_id: Optional[str] = None
    rating: int
    comment: Optional[str] = None
    created_at: Optional[str] = None
