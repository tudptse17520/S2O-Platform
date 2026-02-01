from pydantic import BaseModel, Field
from typing import Optional


class CreatePromotionRequest(BaseModel):
    code: str = Field(..., min_length=1, max_length=50)
    type: str = Field(..., description="Promotion type: PERCENTAGE, FIXED_AMOUNT, BUY_ONE_GET_ONE")
    value: float = Field(..., gt=0)
    start_date: str = Field(..., description="Start date in ISO format")
    end_date: str = Field(..., description="End date in ISO format")


class UpdatePromotionRequest(BaseModel):
    code: Optional[str] = Field(None, min_length=1, max_length=50)
    type: Optional[str] = None
    value: Optional[float] = Field(None, gt=0)
    start_date: Optional[str] = None
    end_date: Optional[str] = None


class ApplyPromotionRequest(BaseModel):
    code: str
    amount: float = Field(..., gt=0)


class PromotionResponse(BaseModel):
    id: str
    tenant_id: str
    code: str
    type: str
    value: float
    start_date: str
    end_date: str
    is_active: bool
    is_expired: bool


class ApplyPromotionResponse(BaseModel):
    original_amount: float
    discount: float
    final_amount: float
    promotion: PromotionResponse
