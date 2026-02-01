import uuid
from datetime import datetime
from typing import List, Optional, Dict, Any

from ..domain.interfaces.iinvoice_repository import IInvoiceRepository
from ..domain.models.invoice import Invoice, PaymentStatus, PaymentMethod


class InvoiceService:
    """Service layer for Invoice operations"""
    
    def __init__(self, invoice_repo: IInvoiceRepository):
        self.invoice_repo = invoice_repo

    def create_invoice(self, tenant_id: str, order_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new invoice"""
        invoice_id = uuid.uuid4()
        
        invoice = Invoice(
            id=str(invoice_id),
            tenant_id=tenant_id,
            order_id=order_id,
            final_amount=data.get('final_amount', 0),
            tax_amount=data.get('tax_amount', 0),
            discount_amount=data.get('discount_amount', 0),
            payment_method=data.get('payment_method', PaymentMethod.CASH),
            payment_status=PaymentStatus.PENDING,
            issued_at=datetime.utcnow()
        )
        
        saved_invoice = self.invoice_repo.create(invoice)
        return self._to_dict(saved_invoice)

    def get_invoice(self, invoice_id: str) -> Optional[Dict[str, Any]]:
        """Get an invoice by ID"""
        invoice = self.invoice_repo.get_by_id(invoice_id)
        if invoice:
            return self._to_dict(invoice)
        return None

    def get_invoice_by_order(self, order_id: str) -> List[Dict[str, Any]]:
        """Get invoices for an order"""
        invoices = self.invoice_repo.get_by_order(order_id)
        return [self._to_dict(i) for i in invoices]

    def get_invoices_by_tenant(self, tenant_id: str) -> List[Dict[str, Any]]:
        """Get all invoices for a tenant"""
        invoices = self.invoice_repo.get_by_tenant(tenant_id)
        return [self._to_dict(i) for i in invoices]

    def get_invoices_by_status(self, tenant_id: str, status: str) -> List[Dict[str, Any]]:
        """Get invoices by status"""
        invoices = self.invoice_repo.get_by_status(tenant_id, status)
        return [self._to_dict(i) for i in invoices]

    def mark_paid(self, invoice_id: str) -> Dict[str, Any]:
        """Mark invoice as paid"""
        invoice = self.invoice_repo.get_by_id(invoice_id)
        if not invoice:
            raise ValueError(f"Invoice with id {invoice_id} not found")
        
        invoice.payment_status = PaymentStatus.PAID
        updated_invoice = self.invoice_repo.update(invoice_id, invoice)
        return self._to_dict(updated_invoice)

    def mark_failed(self, invoice_id: str) -> Dict[str, Any]:
        """Mark invoice payment as failed"""
        invoice = self.invoice_repo.get_by_id(invoice_id)
        if not invoice:
            raise ValueError(f"Invoice with id {invoice_id} not found")
        
        invoice.payment_status = PaymentStatus.FAILED
        updated_invoice = self.invoice_repo.update(invoice_id, invoice)
        return self._to_dict(updated_invoice)

    def refund(self, invoice_id: str) -> Dict[str, Any]:
        """Refund an invoice"""
        invoice = self.invoice_repo.get_by_id(invoice_id)
        if not invoice:
            raise ValueError(f"Invoice with id {invoice_id} not found")
        
        if invoice.payment_status != PaymentStatus.PAID.value and invoice.payment_status != "PAID":
            raise ValueError("Can only refund paid invoices")
        
        invoice.payment_status = PaymentStatus.REFUNDED
        updated_invoice = self.invoice_repo.update(invoice_id, invoice)
        return self._to_dict(updated_invoice)

    def _to_dict(self, invoice: Invoice) -> Dict[str, Any]:
        """Convert invoice entity to dictionary"""
        return {
            "id": str(invoice.id),
            "tenant_id": str(invoice.tenant_id),
            "order_id": str(invoice.order_id),
            "final_amount": invoice.final_amount,
            "tax_amount": invoice.tax_amount,
            "discount_amount": invoice.discount_amount,
            "total_amount": invoice.get_total_amount(),
            "payment_method": invoice.payment_method if isinstance(invoice.payment_method, str) else invoice.payment_method.value,
            "payment_status": invoice.payment_status if isinstance(invoice.payment_status, str) else invoice.payment_status.value,
            "issued_at": invoice.issued_at.isoformat() if invoice.issued_at else None
        }
