from pydantic import BaseModel, Field
from typing import Optional


class CreateInvoiceRequest(BaseModel):
    order_id: str
    final_amount: float = Field(..., gt=0)
    tax_amount: Optional[float] = 0
    discount_amount: Optional[float] = 0
    payment_method: Optional[str] = "CASH"


class UpdatePaymentStatusRequest(BaseModel):
    status: str = Field(..., description="Payment status: PENDING, PAID, FAILED, REFUNDED")


class InvoiceResponse(BaseModel):
    id: str
    tenant_id: str
    order_id: str
    final_amount: float
    tax_amount: float
    discount_amount: float
    total_amount: float
    payment_method: str
    payment_status: str
    issued_at: Optional[str] = None
