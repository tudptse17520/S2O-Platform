from typing import List, Optional, Dict, Any
import uuid

from ..domain.interfaces.icustomer_repository import ICustomerRepository
from ..domain.models.customer import Customer


class CustomerService:
    """Service for customer-related business logic"""
    
    def __init__(self, customer_repo: ICustomerRepository):
        self.customer_repo = customer_repo
    
    def create_customer(self, user_id: str, tenant_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new customer profile"""
        customer = Customer(
            user_id=user_id,
            phone_number=data.get('phone_number'),
            loyalty_points=0,
        )
        
        created = self.customer_repo.create(customer, tenant_id)
        return self._to_dict(created)
    
    def get_customer(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get customer by user ID"""
        customer = self.customer_repo.get_by_user_id(user_id)
        return self._to_dict(customer) if customer else None
    
    def get_customers_by_tenant(self, tenant_id: str) -> List[Dict[str, Any]]:
        """Get all customers for a tenant"""
        customers = self.customer_repo.get_by_tenant(tenant_id)
        return [self._to_dict(c) for c in customers]
    
    def update_customer(self, user_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update customer profile"""
        customer = self.customer_repo.get_by_user_id(user_id)
        if not customer:
            raise ValueError(f"Customer not found for user {user_id}")
        
        if 'phone_number' in data:
            customer.phone_number = data['phone_number']
        
        updated = self.customer_repo.update(user_id, customer)
        return self._to_dict(updated)
    
    def add_loyalty_points(self, user_id: str, points: int) -> Dict[str, Any]:
        """Add loyalty points to customer"""
        if points <= 0:
            raise ValueError("Points must be positive")
        
        updated = self.customer_repo.add_loyalty_points(user_id, points)
        return self._to_dict(updated)
    
    def redeem_loyalty_points(self, user_id: str, points: int) -> Dict[str, Any]:
        """Redeem loyalty points"""
        if points <= 0:
            raise ValueError("Points must be positive")
        
        success = self.customer_repo.redeem_loyalty_points(user_id, points)
        if not success:
            raise ValueError("Insufficient loyalty points")
        
        customer = self.customer_repo.get_by_user_id(user_id)
        return self._to_dict(customer)
    
    def delete_customer(self, user_id: str) -> bool:
        """Delete customer profile"""
        return self.customer_repo.delete(user_id)
    
    def _to_dict(self, customer: Customer) -> Dict[str, Any]:
        return {
            "user_id": customer.user_id,
            "phone_number": customer.phone_number,
            "loyalty_points": customer.loyalty_points,
        }
