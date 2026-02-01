from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class CreateReservationRequest(BaseModel):
    branch_id: str
    booking_time: str = Field(..., description="ISO format datetime")
    party_size: int = Field(1, ge=1)


class UpdateReservationRequest(BaseModel):
    booking_time: Optional[str] = None
    party_size: Optional[int] = Field(None, ge=1)


class UpdateReservationStatusRequest(BaseModel):
    status: str = Field(..., description="Reservation status: PENDING, CONFIRMED, CANCELLED, COMPLETED")


class ReservationResponse(BaseModel):
    id: str
    tenant_id: str
    branch_id: str
    user_id: str
    booking_time: str
    party_size: int
    status: str
    created_at: Optional[str] = None
