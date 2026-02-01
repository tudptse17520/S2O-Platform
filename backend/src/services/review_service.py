import uuid
from datetime import datetime
from typing import List, Optional, Dict, Any

from ..domain.interfaces.ireview_repository import IReviewRepository
from ..domain.models.review import Review


class ReviewService:
    """Service layer for Review operations"""
    
    def __init__(self, review_repo: IReviewRepository):
        self.review_repo = review_repo

    def create_review(self, user_id: str, tenant_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new review"""
        review_id = uuid.uuid4()
        
        rating = data.get('rating', 5)
        if rating < 1 or rating > 5:
            raise ValueError("Rating must be between 1 and 5")
        
        review = Review(
            id=str(review_id),
            user_id=user_id,
            tenant_id=tenant_id,
            order_id=data.get('order_id'),
            rating=rating,
            comment=data.get('comment'),
            created_at=datetime.utcnow()
        )
        
        saved_review = self.review_repo.create(review)
        return self._to_dict(saved_review)

    def get_review(self, review_id: str) -> Optional[Dict[str, Any]]:
        """Get a review by ID"""
        review = self.review_repo.get_by_id(review_id)
        if review:
            return self._to_dict(review)
        return None

    def get_reviews_by_tenant(self, tenant_id: str) -> List[Dict[str, Any]]:
        """Get all reviews for a tenant"""
        reviews = self.review_repo.get_by_tenant(tenant_id)
        return [self._to_dict(r) for r in reviews]

    def get_reviews_by_user(self, user_id: str) -> List[Dict[str, Any]]:
        """Get all reviews by a user"""
        reviews = self.review_repo.get_by_user(user_id)
        return [self._to_dict(r) for r in reviews]

    def update_review(self, review_id: str, user_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update a review"""
        existing = self.review_repo.get_by_id(review_id)
        if not existing:
            raise ValueError(f"Review with id {review_id} not found")
        
        # Only the author can update their review
        if str(existing.user_id) != str(user_id):
            raise ValueError("You can only update your own reviews")
        
        if 'rating' in data:
            rating = data['rating']
            if rating < 1 or rating > 5:
                raise ValueError("Rating must be between 1 and 5")
            existing.rating = rating
        
        if 'comment' in data:
            existing.comment = data['comment']
        
        updated_review = self.review_repo.update(review_id, existing)
        return self._to_dict(updated_review)

    def delete_review(self, review_id: str, user_id: str) -> bool:
        """Delete a review"""
        existing = self.review_repo.get_by_id(review_id)
        if not existing:
            raise ValueError(f"Review with id {review_id} not found")
        
        # Only the author can delete their review
        if str(existing.user_id) != str(user_id):
            raise ValueError("You can only delete your own reviews")
        
        return self.review_repo.delete(review_id)
    
    def get_average_rating(self, tenant_id: str) -> float:
        """Calculate average rating for a tenant"""
        reviews = self.review_repo.get_by_tenant(tenant_id)
        if not reviews:
            return 0.0
        total = sum(r.rating for r in reviews)
        return round(total / len(reviews), 2)

    def _to_dict(self, review: Review) -> Dict[str, Any]:
        """Convert review entity to dictionary"""
        return {
            "id": str(review.id),
            "user_id": str(review.user_id),
            "tenant_id": str(review.tenant_id),
            "order_id": str(review.order_id) if review.order_id else None,
            "rating": review.rating,
            "comment": review.comment,
            "created_at": review.created_at.isoformat() if review.created_at else None
        }
