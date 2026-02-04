from typing import List, Optional
import uuid
from sqlalchemy.orm import Session

from ...domain.interfaces.icustomer_repository import ICustomerRepository
from ...domain.models.customer import Customer
from ..models.customer_model import Customer as CustomerModel


class CustomerRepository(ICustomerRepository):
    """Repository implementation for Customer entity"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def _to_domain(self, model: CustomerModel) -> Customer:
        return Customer(
            user_id=str(model.user_id),
            phone_number=model.phone_number,
            loyalty_points=model.loyalty_points,
        )
    
    def _to_orm(self, customer: Customer, tenant_id: str = None) -> CustomerModel:
        model = CustomerModel()
        model.id = uuid.uuid4()
        model.user_id = uuid.UUID(customer.user_id)
        model.tenant_id = uuid.UUID(tenant_id) if tenant_id else None
        model.phone_number = customer.phone_number
        model.loyalty_points = customer.loyalty_points
        return model
    
    def create(self, customer: Customer, tenant_id: str = None) -> Customer:
        model = self._to_orm(customer, tenant_id)
        self.db.add(model)
        self.db.flush()
        return self._to_domain(model)
    
    def get_by_user_id(self, user_id: str) -> Optional[Customer]:
        model = self.db.query(CustomerModel).filter(
            CustomerModel.user_id == uuid.UUID(user_id)
        ).first()
        return self._to_domain(model) if model else None
    
    def get_by_tenant(self, tenant_id: str) -> List[Customer]:
        models = self.db.query(CustomerModel).filter(
            CustomerModel.tenant_id == uuid.UUID(tenant_id)
        ).all()
        return [self._to_domain(m) for m in models]
    
    def get_all(self) -> List[Customer]:
        models = self.db.query(CustomerModel).all()
        return [self._to_domain(m) for m in models]
    
    def update(self, user_id: str, customer: Customer) -> Customer:
        model = self.db.query(CustomerModel).filter(
            CustomerModel.user_id == uuid.UUID(user_id)
        ).first()
        if not model:
            raise ValueError(f"Customer for user {user_id} not found")
        
        model.phone_number = customer.phone_number
        model.loyalty_points = customer.loyalty_points
        self.db.flush()
        return self._to_domain(model)
    
    def delete(self, user_id: str) -> bool:
        model = self.db.query(CustomerModel).filter(
            CustomerModel.user_id == uuid.UUID(user_id)
        ).first()
        if model:
            self.db.delete(model)
            return True
        return False
    
    def add_loyalty_points(self, user_id: str, points: int) -> Customer:
        model = self.db.query(CustomerModel).filter(
            CustomerModel.user_id == uuid.UUID(user_id)
        ).first()
        if not model:
            raise ValueError(f"Customer for user {user_id} not found")
        
        model.loyalty_points += points
        self.db.flush()
        return self._to_domain(model)
    
    def redeem_loyalty_points(self, user_id: str, points: int) -> bool:
        model = self.db.query(CustomerModel).filter(
            CustomerModel.user_id == uuid.UUID(user_id)
        ).first()
        if not model:
            raise ValueError(f"Customer for user {user_id} not found")
        
        if model.loyalty_points >= points:
            model.loyalty_points -= points
            self.db.flush()
            return True
        return False
