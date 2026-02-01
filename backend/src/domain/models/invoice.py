from typing import Optional
from datetime import datetime
from enum import Enum


class PaymentStatus(str, Enum):
    """Enum for payment statuses"""
    PENDING = "PENDING"
    PAID = "PAID"
    FAILED = "FAILED"
    REFUNDED = "REFUNDED"


class PaymentMethod(str, Enum):
    """Enum for payment methods"""
    CASH = "CASH"
    CARD = "CARD"
    VIETQR = "VIETQR"
    BANK_TRANSFER = "BANK_TRANSFER"
    DIGITAL_WALLET = "DIGITAL_WALLET"


class Invoice:
    """
    Domain Model for Invoice
    
    Represents a payment invoice.
    One Order can have multiple Invoices (split billing support).
    Attributes map to the 'invoices' table in DRD.
    """
    
    def __init__(
        self,
        id: str,
        tenant_id: str,
        order_id: str,
        final_amount: float,
        tax_amount: float = 0,
        discount_amount: float = 0,
        payment_method: str = PaymentMethod.CASH,
        payment_status: str = PaymentStatus.PENDING,
        issued_at: Optional[datetime] = None
    ):
        self.id = id
        self.tenant_id = tenant_id
        self.order_id = order_id
        self.final_amount = final_amount
        self.tax_amount = tax_amount
        self.discount_amount = discount_amount
        self.payment_method = payment_method
        self.payment_status = payment_status
        self.issued_at = issued_at or datetime.utcnow()
    
    def mark_paid(self) -> None:
        """Mark invoice as paid"""
        self.payment_status = PaymentStatus.PAID
    
    def mark_failed(self) -> None:
        """Mark invoice payment as failed"""
        self.payment_status = PaymentStatus.FAILED
    
    def refund(self) -> None:
        """Refund the invoice"""
        self.payment_status = PaymentStatus.REFUNDED
    
    def get_total_amount(self) -> float:
        """Calculate total amount (final_amount + tax - discount)"""
        return self.final_amount + self.tax_amount - self.discount_amount
    
    def is_valid(self) -> bool:
        """Validate invoice data"""
        return (
            self.final_amount > 0 
            and self.tenant_id 
            and self.order_id
        )
    
    def __repr__(self) -> str:
        return f"<Invoice id={self.id} order_id={self.order_id} amount={self.final_amount} status={self.payment_status}>"
