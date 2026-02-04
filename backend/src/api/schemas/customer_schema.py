from pydantic import BaseModel, Field
from typing import Optional


class CreateCustomerRequest(BaseModel):
    phone_number: Optional[str] = None


class UpdateCustomerRequest(BaseModel):
    phone_number: Optional[str] = None


class AddLoyaltyPointsRequest(BaseModel):
    points: int = Field(..., gt=0, description="Number of points to add")


class RedeemLoyaltyPointsRequest(BaseModel):
    points: int = Field(..., gt=0, description="Number of points to redeem")


class CustomerResponse(BaseModel):
    user_id: str
    phone_number: Optional[str]
    loyalty_points: int
