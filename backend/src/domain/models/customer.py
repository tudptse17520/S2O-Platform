from typing import Optional


class Customer:
    """
    Domain Model for Customer
    
    Represents a customer profile linked to a User.
    One-to-One relationship with User.
    Attributes map to the 'customers' table in DRD.
    """
    
    def __init__(
        self,
        user_id: str,
        phone_number: Optional[str] = None,
        loyalty_points: int = 0
    ):
        self.user_id = user_id
        self.phone_number = phone_number
        self.loyalty_points = loyalty_points
    
    def add_loyalty_points(self, points: int) -> None:
        """Add loyalty points to customer account"""
        if points > 0:
            self.loyalty_points += points
    
    def redeem_loyalty_points(self, points: int) -> bool:
        """
        Redeem loyalty points
        
        Returns:
            bool: True if redemption successful, False if insufficient points
        """
        if self.loyalty_points >= points:
            self.loyalty_points -= points
            return True
        return False
    
    def is_valid(self) -> bool:
        """Validate customer data"""
        return self.user_id and self.loyalty_points >= 0
    
    def __repr__(self) -> str:
        return f"<Customer user_id={self.user_id} loyalty_points={self.loyalty_points}>"
