from pydantic import BaseModel, Field
from typing import Optional


class ProcessPaymentRequest(BaseModel):
    invoice_id: str
    payment_method: str = Field(..., description="Payment method: CASH, CREDIT_CARD, QR_CODE, E_WALLET")
    amount: float = Field(..., gt=0)


class PaymentResponse(BaseModel):
    id: str
    invoice_id: str
    amount: float
    payment_method: str
    status: str
    transaction_id: Optional[str] = None
    created_at: Optional[str] = None


class PaymentQRResponse(BaseModel):
    invoice_id: str
    qr_code_url: str
    amount: float
    expires_at: Optional[str] = None
