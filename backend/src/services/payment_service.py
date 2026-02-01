from typing import List, Optional, Dict, Any
import uuid
from datetime import datetime

from ..domain.interfaces.ipayment_repository import IPaymentRepository
from ..domain.models.payment import Payment, PaymentStatus


class PaymentService:
    """Service for payment-related business logic"""
    
    def __init__(self, payment_repo: IPaymentRepository):
        self.payment_repo = payment_repo
    
    def create_payment(self, tenant_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new payment"""
        payment = Payment(
            id=str(uuid.uuid4()),
            tenant_id=tenant_id,
            order_id=data.get('order_id'),
            invoice_id=data.get('invoice_id'),
            amount=data.get('amount', 0.0),
            method=data.get('method', 'VIETQR'),
            status=PaymentStatus.PENDING,
        )
        
        created = self.payment_repo.create(payment)
        return self._to_dict(created)
    
    def get_payment(self, payment_id: str) -> Optional[Dict[str, Any]]:
        """Get payment by ID"""
        payment = self.payment_repo.get_by_id(payment_id)
        return self._to_dict(payment) if payment else None
    
    def get_payments_by_tenant(self, tenant_id: str) -> List[Dict[str, Any]]:
        """Get all payments for a tenant"""
        payments = self.payment_repo.get_by_tenant(tenant_id)
        return [self._to_dict(p) for p in payments]
    
    def get_payments_by_order(self, order_id: str) -> List[Dict[str, Any]]:
        """Get payments for an order"""
        payments = self.payment_repo.get_by_order(order_id)
        return [self._to_dict(p) for p in payments]
    
    def get_payments_by_invoice(self, invoice_id: str) -> List[Dict[str, Any]]:
        """Get payments for an invoice"""
        payments = self.payment_repo.get_by_invoice(invoice_id)
        return [self._to_dict(p) for p in payments]
    
    def process_payment(self, payment_id: str) -> Dict[str, Any]:
        """Process a payment (mark as success)"""
        payment = self.payment_repo.get_by_id(payment_id)
        if not payment:
            raise ValueError(f"Payment {payment_id} not found")
        
        payment.mark_success()
        updated = self.payment_repo.update(payment_id, payment)
        return self._to_dict(updated)
    
    def mark_failed(self, payment_id: str) -> Dict[str, Any]:
        """Mark payment as failed"""
        payment = self.payment_repo.get_by_id(payment_id)
        if not payment:
            raise ValueError(f"Payment {payment_id} not found")
        
        payment.mark_failed()
        updated = self.payment_repo.update(payment_id, payment)
        return self._to_dict(updated)
    
    def refund_payment(self, payment_id: str) -> Dict[str, Any]:
        """Refund a payment"""
        payment = self.payment_repo.get_by_id(payment_id)
        if not payment:
            raise ValueError(f"Payment {payment_id} not found")
        
        if payment.status != PaymentStatus.SUCCESS:
            raise ValueError("Can only refund successful payments")
        
        refunded = self.payment_repo.refund(payment_id, payment.amount)
        return self._to_dict(refunded)
    
    def generate_qr_code(self, payment_id: str, tenant_id: str) -> Dict[str, Any]:
        """Generate VietQR code for payment"""
        payment = self.payment_repo.get_by_id(payment_id)
        if not payment:
            raise ValueError(f"Payment {payment_id} not found")
        
        # Generate QR code URL (placeholder - integrate with VietQR API)
        qr_url = f"https://img.vietqr.io/image/970436-ACCOUNT-qr_only.png?amount={payment.amount}&addInfo=Payment_{payment_id}"
        
        return {
            "payment_id": payment_id,
            "amount": payment.amount,
            "qr_url": qr_url,
            "status": payment.status,
        }
    
    def _to_dict(self, payment: Payment) -> Dict[str, Any]:
        return {
            "id": payment.id,
            "tenant_id": payment.tenant_id,
            "order_id": payment.order_id,
            "invoice_id": payment.invoice_id,
            "amount": payment.amount,
            "method": payment.method,
            "status": payment.status,
            "created_at": payment.created_at.isoformat() if payment.created_at else None,
            "updated_at": payment.updated_at.isoformat() if payment.updated_at else None,
        }
