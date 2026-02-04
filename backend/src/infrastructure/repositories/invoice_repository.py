from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from ...domain.interfaces.iinvoice_repository import IInvoiceRepository
from ...domain.models.invoice import Invoice as DomainInvoice
from ...infrastructure.models import Invoice as ORMInvoice, PaymentStatus as ORMPaymentStatus, PaymentMethod as ORMPaymentMethod


class InvoiceRepository(IInvoiceRepository):
    """SQLAlchemy implementation of IInvoiceRepository"""
    
    def __init__(self, session: Session):
        self.session = session

    def _to_domain(self, orm_invoice: ORMInvoice) -> DomainInvoice:
        """Convert ORM model to domain model"""
        return DomainInvoice(
            id=str(orm_invoice.id),
            tenant_id=str(orm_invoice.tenant_id),
            order_id=str(orm_invoice.order_id),
            final_amount=orm_invoice.final_amount,
            payment_method=orm_invoice.payment_method.value if orm_invoice.payment_method else "CASH",
            payment_status=orm_invoice.payment_status.value if orm_invoice.payment_status else "PENDING",
            issued_at=orm_invoice.created_at
        )

    def _to_orm(self, domain_invoice: DomainInvoice) -> ORMInvoice:
        """Convert domain model to ORM model"""
        # Map domain payment method to ORM
        method_map = {
            "CASH": ORMPaymentMethod.CASH,
            "CARD": ORMPaymentMethod.CREDIT_CARD,
            "CREDIT_CARD": ORMPaymentMethod.CREDIT_CARD,
            "VIETQR": ORMPaymentMethod.QR_CODE,
            "QR_CODE": ORMPaymentMethod.QR_CODE,
            "BANK_TRANSFER": ORMPaymentMethod.E_WALLET,
            "DIGITAL_WALLET": ORMPaymentMethod.E_WALLET,
            "E_WALLET": ORMPaymentMethod.E_WALLET
        }
        return ORMInvoice(
            id=domain_invoice.id,
            tenant_id=domain_invoice.tenant_id,
            order_id=domain_invoice.order_id,
            final_amount=domain_invoice.final_amount,
            payment_method=method_map.get(domain_invoice.payment_method, ORMPaymentMethod.CASH),
            payment_status=ORMPaymentStatus(domain_invoice.payment_status) if domain_invoice.payment_status else ORMPaymentStatus.PENDING,
            created_at=domain_invoice.issued_at,
            updated_at=datetime.utcnow()
        )

    def create(self, invoice: DomainInvoice) -> DomainInvoice:
        """Create a new invoice"""
        orm_invoice = self._to_orm(invoice)
        self.session.add(orm_invoice)
        self.session.flush()
        return invoice

    def get_by_id(self, invoice_id: str) -> Optional[DomainInvoice]:
        """Get invoice by ID"""
        orm = self.session.query(ORMInvoice).filter_by(id=invoice_id).first()
        if orm:
            return self._to_domain(orm)
        return None

    def get_all(self) -> List[DomainInvoice]:
        """Get all invoices"""
        orm_list = self.session.query(ORMInvoice).all()
        return [self._to_domain(i) for i in orm_list]

    def get_by_order(self, order_id: str) -> List[DomainInvoice]:
        """Get all invoices for an order (split billing support)"""
        orm_list = self.session.query(ORMInvoice).filter_by(order_id=order_id).all()
        return [self._to_domain(i) for i in orm_list]

    def get_by_tenant(self, tenant_id: str) -> List[DomainInvoice]:
        """Get all invoices for a tenant"""
        orm_list = self.session.query(ORMInvoice).filter_by(tenant_id=tenant_id).all()
        return [self._to_domain(i) for i in orm_list]

    def update(self, invoice_id: str, invoice: DomainInvoice) -> DomainInvoice:
        """Update invoice"""
        orm = self.session.query(ORMInvoice).filter_by(id=invoice_id).first()
        if orm:
            orm.final_amount = invoice.final_amount
            orm.payment_status = ORMPaymentStatus(invoice.payment_status) if invoice.payment_status else orm.payment_status
            orm.updated_at = datetime.utcnow()
            self.session.flush()
            return self._to_domain(orm)
        raise ValueError(f"Invoice with id {invoice_id} not found")

    def delete(self, invoice_id: str) -> bool:
        """Delete invoice"""
        orm = self.session.query(ORMInvoice).filter_by(id=invoice_id).first()
        if orm:
            self.session.delete(orm)
            self.session.flush()
            return True
        return False

    def get_by_status(self, tenant_id: str, status: str) -> List[DomainInvoice]:
        """Get invoices by payment status"""
        orm_list = self.session.query(ORMInvoice).filter_by(
            tenant_id=tenant_id,
            payment_status=ORMPaymentStatus(status)
        ).all()
        return [self._to_domain(i) for i in orm_list]
