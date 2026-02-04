from typing import List, Optional
import uuid
from sqlalchemy.orm import Session

from ...domain.interfaces.ipayment_repository import IPaymentRepository
from ...domain.models.payment import Payment, PaymentStatus, PaymentMethod
from ..models.payment_model import Payment as PaymentModel, PaymentStatusEnum, PaymentMethodEnum


class PaymentRepository(IPaymentRepository):
    """Repository implementation for Payment entity"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def _method_to_enum(self, method: str) -> PaymentMethodEnum:
        method_map = {
            "CASH": PaymentMethodEnum.CASH,
            "CARD": PaymentMethodEnum.CARD,
            "VIETQR": PaymentMethodEnum.VIETQR,
            "BANK_TRANSFER": PaymentMethodEnum.BANK_TRANSFER,
        }
        return method_map.get(method, PaymentMethodEnum.VIETQR)
    
    def _status_to_enum(self, status: str) -> PaymentStatusEnum:
        status_map = {
            "PENDING": PaymentStatusEnum.PENDING,
            "SUCCESS": PaymentStatusEnum.SUCCESS,
            "FAILED": PaymentStatusEnum.FAILED,
            "REFUNDED": PaymentStatusEnum.REFUNDED,
        }
        return status_map.get(status, PaymentStatusEnum.PENDING)
    
    def _to_domain(self, model: PaymentModel) -> Payment:
        return Payment(
            id=str(model.id),
            tenant_id=str(model.tenant_id),
            order_id=str(model.order_id) if model.order_id else None,
            invoice_id=str(model.invoice_id) if model.invoice_id else None,
            amount=model.amount,
            method=model.method.value if model.method else PaymentMethod.VIETQR,
            status=model.status.value if model.status else PaymentStatus.PENDING,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
    
    def _to_orm(self, payment: Payment) -> PaymentModel:
        model = PaymentModel()
        model.id = uuid.UUID(payment.id)
        model.tenant_id = uuid.UUID(payment.tenant_id)
        model.order_id = uuid.UUID(payment.order_id) if payment.order_id else None
        model.invoice_id = uuid.UUID(payment.invoice_id) if payment.invoice_id else None
        model.amount = payment.amount
        model.method = self._method_to_enum(payment.method)
        model.status = self._status_to_enum(payment.status)
        return model
    
    def create(self, payment: Payment) -> Payment:
        model = self._to_orm(payment)
        self.db.add(model)
        self.db.flush()
        return self._to_domain(model)
    
    def get_by_id(self, payment_id: str) -> Optional[Payment]:
        model = self.db.query(PaymentModel).filter(
            PaymentModel.id == uuid.UUID(payment_id)
        ).first()
        return self._to_domain(model) if model else None
    
    def get_all(self) -> List[Payment]:
        models = self.db.query(PaymentModel).all()
        return [self._to_domain(m) for m in models]
    
    def get_by_order(self, order_id: str) -> List[Payment]:
        models = self.db.query(PaymentModel).filter(
            PaymentModel.order_id == uuid.UUID(order_id)
        ).all()
        return [self._to_domain(m) for m in models]
    
    def get_by_tenant(self, tenant_id: str) -> List[Payment]:
        models = self.db.query(PaymentModel).filter(
            PaymentModel.tenant_id == uuid.UUID(tenant_id)
        ).all()
        return [self._to_domain(m) for m in models]
    
    def get_by_invoice(self, invoice_id: str) -> List[Payment]:
        models = self.db.query(PaymentModel).filter(
            PaymentModel.invoice_id == uuid.UUID(invoice_id)
        ).all()
        return [self._to_domain(m) for m in models]
    
    def update(self, payment_id: str, payment: Payment) -> Payment:
        model = self.db.query(PaymentModel).filter(
            PaymentModel.id == uuid.UUID(payment_id)
        ).first()
        if not model:
            raise ValueError(f"Payment {payment_id} not found")
        
        model.amount = payment.amount
        model.method = self._method_to_enum(payment.method)
        model.status = self._status_to_enum(payment.status)
        self.db.flush()
        return self._to_domain(model)
    
    def refund(self, payment_id: str, amount: float) -> Payment:
        model = self.db.query(PaymentModel).filter(
            PaymentModel.id == uuid.UUID(payment_id)
        ).first()
        if not model:
            raise ValueError(f"Payment {payment_id} not found")
        
        model.status = PaymentStatusEnum.REFUNDED
        self.db.flush()
        return self._to_domain(model)
    
    def delete(self, payment_id: str) -> bool:
        model = self.db.query(PaymentModel).filter(
            PaymentModel.id == uuid.UUID(payment_id)
        ).first()
        if model:
            self.db.delete(model)
            return True
        return False
