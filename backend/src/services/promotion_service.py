import uuid
from datetime import datetime, date
from typing import List, Optional, Dict, Any

from ..domain.interfaces.ipromotion_repository import IPromotionRepository
from ..domain.models.promotion import Promotion, PromotionType


class PromotionService:
    """Service layer for Promotion operations"""
    
    def __init__(self, promotion_repo: IPromotionRepository):
        self.promotion_repo = promotion_repo

    def create_promotion(self, tenant_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new promotion"""
        promotion_id = uuid.uuid4()
        
        # Parse dates
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        
        if isinstance(start_date, str):
            start_date = datetime.fromisoformat(start_date.replace('Z', '+00:00')).date()
        elif isinstance(start_date, datetime):
            start_date = start_date.date()
        else:
            start_date = date.today()
        
        if isinstance(end_date, str):
            end_date = datetime.fromisoformat(end_date.replace('Z', '+00:00')).date()
        elif isinstance(end_date, datetime):
            end_date = end_date.date()
        else:
            end_date = date.today()
        
        promotion = Promotion(
            id=str(promotion_id),
            tenant_id=tenant_id,
            code=data['code'],
            promotion_type=data.get('type', PromotionType.PERCENTAGE),
            value=data['value'],
            start_date=start_date,
            end_date=end_date
        )
        
        saved_promotion = self.promotion_repo.create(promotion)
        return self._to_dict(saved_promotion)

    def get_promotion(self, promotion_id: str) -> Optional[Dict[str, Any]]:
        """Get a promotion by ID"""
        promotion = self.promotion_repo.get_by_id(promotion_id)
        if promotion:
            return self._to_dict(promotion)
        return None

    def get_promotion_by_code(self, tenant_id: str, code: str) -> Optional[Dict[str, Any]]:
        """Get a promotion by code"""
        promotion = self.promotion_repo.get_by_code(tenant_id, code)
        if promotion:
            return self._to_dict(promotion)
        return None

    def get_promotions_by_tenant(self, tenant_id: str) -> List[Dict[str, Any]]:
        """Get all promotions for a tenant"""
        promotions = self.promotion_repo.get_by_tenant(tenant_id)
        return [self._to_dict(p) for p in promotions]

    def get_active_promotions(self, tenant_id: str) -> List[Dict[str, Any]]:
        """Get active promotions for a tenant"""
        promotions = self.promotion_repo.get_active_promotions(tenant_id)
        return [self._to_dict(p) for p in promotions]

    def apply_promotion(self, tenant_id: str, code: str, amount: float) -> Dict[str, Any]:
        """Apply a promotion code to an amount"""
        promotion = self.promotion_repo.get_by_code(tenant_id, code)
        if not promotion:
            raise ValueError(f"Promotion with code {code} not found")
        
        if not promotion.is_active():
            raise ValueError("This promotion is not active")
        
        discount = promotion.calculate_discount(amount)
        final_amount = amount - discount
        
        return {
            "original_amount": amount,
            "discount": discount,
            "final_amount": final_amount,
            "promotion": self._to_dict(promotion)
        }

    def update_promotion(self, promotion_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update a promotion"""
        existing = self.promotion_repo.get_by_id(promotion_id)
        if not existing:
            raise ValueError(f"Promotion with id {promotion_id} not found")
        
        if 'code' in data:
            existing.code = data['code']
        if 'type' in data:
            existing.promotion_type = data['type']
        if 'value' in data:
            existing.value = data['value']
        if 'start_date' in data:
            start_date = data['start_date']
            if isinstance(start_date, str):
                start_date = datetime.fromisoformat(start_date.replace('Z', '+00:00')).date()
            existing.start_date = start_date
        if 'end_date' in data:
            end_date = data['end_date']
            if isinstance(end_date, str):
                end_date = datetime.fromisoformat(end_date.replace('Z', '+00:00')).date()
            existing.end_date = end_date
        
        updated_promotion = self.promotion_repo.update(promotion_id, existing)
        return self._to_dict(updated_promotion)

    def delete_promotion(self, promotion_id: str) -> bool:
        """Delete a promotion"""
        return self.promotion_repo.delete(promotion_id)

    def _to_dict(self, promotion: Promotion) -> Dict[str, Any]:
        """Convert promotion entity to dictionary"""
        return {
            "id": str(promotion.id),
            "tenant_id": str(promotion.tenant_id),
            "code": promotion.code,
            "type": promotion.promotion_type if isinstance(promotion.promotion_type, str) else promotion.promotion_type.value,
            "value": promotion.value,
            "start_date": promotion.start_date.isoformat() if promotion.start_date else None,
            "end_date": promotion.end_date.isoformat() if promotion.end_date else None,
            "is_active": promotion.is_active(),
            "is_expired": promotion.is_expired()
        }
