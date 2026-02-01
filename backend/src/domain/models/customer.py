from typing import Optional
from enum import Enum


class MembershipTier(str, Enum):
    """Membership tier levels based on loyalty points"""
    IRON = "IRON"
    SILVER = "SILVER"
    GOLD = "GOLD"
    DIAMOND = "DIAMOND"


# Tier thresholds (points needed to reach each tier)
TIER_THRESHOLDS = {
    MembershipTier.IRON: 0,
    MembershipTier.SILVER: 1000,
    MembershipTier.GOLD: 5000,
    MembershipTier.DIAMOND: 15000,
}

# Tier benefits (discount percentage)
TIER_BENEFITS = {
    MembershipTier.IRON: 0,
    MembershipTier.SILVER: 5,
    MembershipTier.GOLD: 10,
    MembershipTier.DIAMOND: 15,
}

# Points multiplier per tier
TIER_MULTIPLIERS = {
    MembershipTier.IRON: 1.0,
    MembershipTier.SILVER: 1.25,
    MembershipTier.GOLD: 1.5,
    MembershipTier.DIAMOND: 2.0,
}


class Customer:
    """
    Domain Model for Customer
    
    Represents a customer profile linked to a User.
    One-to-One relationship with User.
    Includes membership tier system for loyalty program.
    """
    
    def __init__(
        self,
        user_id: str,
        phone_number: Optional[str] = None,
        loyalty_points: int = 0,
        total_spent: float = 0.0,
        membership_tier: str = MembershipTier.IRON
    ):
        self.user_id = user_id
        self.phone_number = phone_number
        self.loyalty_points = loyalty_points
        self.total_spent = total_spent
        self._membership_tier = membership_tier
    
    @property
    def membership_tier(self) -> MembershipTier:
        """Get current membership tier based on loyalty points"""
        return self._calculate_tier()
    
    @membership_tier.setter
    def membership_tier(self, value):
        self._membership_tier = value
    
    def _calculate_tier(self) -> MembershipTier:
        """Calculate tier based on total loyalty points earned"""
        if self.loyalty_points >= TIER_THRESHOLDS[MembershipTier.DIAMOND]:
            return MembershipTier.DIAMOND
        elif self.loyalty_points >= TIER_THRESHOLDS[MembershipTier.GOLD]:
            return MembershipTier.GOLD
        elif self.loyalty_points >= TIER_THRESHOLDS[MembershipTier.SILVER]:
            return MembershipTier.SILVER
        return MembershipTier.IRON
    
    def add_loyalty_points(self, points: int) -> int:
        """
        Add loyalty points with tier multiplier
        Returns actual points added after multiplier
        """
        if points > 0:
            multiplier = TIER_MULTIPLIERS.get(self.membership_tier, 1.0)
            actual_points = int(points * multiplier)
            self.loyalty_points += actual_points
            return actual_points
        return 0
    
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
    
    def get_discount_percentage(self) -> int:
        """Get discount percentage based on current tier"""
        return TIER_BENEFITS.get(self.membership_tier, 0)
    
    def get_points_multiplier(self) -> float:
        """Get points multiplier based on current tier"""
        return TIER_MULTIPLIERS.get(self.membership_tier, 1.0)
    
    def points_to_next_tier(self) -> Optional[int]:
        """Calculate points needed to reach next tier"""
        current = self.membership_tier
        
        if current == MembershipTier.IRON:
            return TIER_THRESHOLDS[MembershipTier.SILVER] - self.loyalty_points
        elif current == MembershipTier.SILVER:
            return TIER_THRESHOLDS[MembershipTier.GOLD] - self.loyalty_points
        elif current == MembershipTier.GOLD:
            return TIER_THRESHOLDS[MembershipTier.DIAMOND] - self.loyalty_points
        
        return None  # Already at max tier
    
    def get_tier_info(self) -> dict:
        """Get comprehensive tier information"""
        return {
            "current_tier": self.membership_tier.value,
            "loyalty_points": self.loyalty_points,
            "discount_percentage": self.get_discount_percentage(),
            "points_multiplier": self.get_points_multiplier(),
            "points_to_next_tier": self.points_to_next_tier(),
            "total_spent": self.total_spent
        }
    
    def add_spending(self, amount: float, points_rate: float = 0.1) -> int:
        """
        Record spending and earn points
        Default: 1 point per 10 currency spent
        
        Returns: Points earned
        """
        if amount > 0:
            self.total_spent += amount
            base_points = int(amount * points_rate)
            return self.add_loyalty_points(base_points)
        return 0
    
    def is_valid(self) -> bool:
        """Validate customer data"""
        return self.user_id and self.loyalty_points >= 0
    
    def __repr__(self) -> str:
        return f"<Customer user_id={self.user_id} tier={self.membership_tier.value} points={self.loyalty_points}>"
