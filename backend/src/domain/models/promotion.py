from typing import Optional
from datetime import date
from enum import Enum


class PromotionType(str, Enum):
    """Enum for promotion types"""
    PERCENTAGE = "PERCENTAGE"  # Discount by percentage
    FIXED_AMOUNT = "FIXED_AMOUNT"  # Discount by fixed amount
    BUY_ONE_GET_ONE = "BUY_ONE_GET_ONE"  # BOGO deal


class Promotion:
    """
    Domain Model for Promotion
    
    Represents a promotional offer/discount.
    Can be applied to specific products.
    Attributes map to the 'promotions' table in DRD.
    """
    
    def __init__(
        self,
        id: str,
        tenant_id: str,
        code: str,
        promotion_type: str,
        value: float,
        start_date: date,
        end_date: date
    ):
        self.id = id
        self.tenant_id = tenant_id
        self.code = code
        self.promotion_type = promotion_type
        self.value = value
        self.start_date = start_date
        self.end_date = end_date
    
    def is_active(self) -> bool:
        """Check if promotion is currently active"""
        today = date.today()
        return self.start_date <= today <= self.end_date
    
    def is_expired(self) -> bool:
        """Check if promotion has expired"""
        return date.today() > self.end_date
    
    def calculate_discount(self, amount: float) -> float:
        """
        Calculate discount amount based on promotion type
        
        Args:
            amount: Original amount to apply discount to
            
        Returns:
            float: Discount amount
        """
        if self.promotion_type == PromotionType.PERCENTAGE:
            return amount * (self.value / 100)
        elif self.promotion_type == PromotionType.FIXED_AMOUNT:
            return min(self.value, amount)  # Don't exceed original amount
        else:
            return 0
    
    def is_valid(self) -> bool:
        """Validate promotion data"""
        return (
            self.code 
            and self.value > 0 
            and self.start_date < self.end_date 
            and self.tenant_id
        )
    
    def __repr__(self) -> str:
        return f"<Promotion id={self.id} code={self.code} type={self.promotion_type} value={self.value}>"
