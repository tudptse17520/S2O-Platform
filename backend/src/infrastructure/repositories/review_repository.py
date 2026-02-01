from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from ...domain.interfaces.ireview_repository import IReviewRepository
from ...domain.models.review import Review as DomainReview
from ...infrastructure.models import Review as ORMReview


class ReviewRepository(IReviewRepository):
    """SQLAlchemy implementation of IReviewRepository"""
    
    def __init__(self, session: Session):
        self.session = session

    def _to_domain(self, orm_review: ORMReview) -> DomainReview:
        """Convert ORM model to domain model"""
        return DomainReview(
            id=str(orm_review.id),
            user_id=str(orm_review.user_id),
            tenant_id=str(orm_review.tenant_id),
            order_id=str(orm_review.order_id) if orm_review.order_id else None,
            rating=orm_review.rating,
            comment=orm_review.comment,
            created_at=orm_review.created_at
        )

    def _to_orm(self, domain_review: DomainReview) -> ORMReview:
        """Convert domain model to ORM model"""
        return ORMReview(
            id=domain_review.id,
            user_id=domain_review.user_id,
            tenant_id=domain_review.tenant_id,
            order_id=domain_review.order_id,
            rating=domain_review.rating,
            comment=domain_review.comment,
            created_at=domain_review.created_at,
            updated_at=datetime.utcnow()
        )

    def create(self, review: DomainReview) -> DomainReview:
        """Create a new review"""
        orm_review = self._to_orm(review)
        self.session.add(orm_review)
        self.session.flush()
        return review

    def get_by_id(self, review_id: str) -> Optional[DomainReview]:
        """Get review by ID"""
        orm = self.session.query(ORMReview).filter_by(id=review_id).first()
        if orm:
            return self._to_domain(orm)
        return None

    def get_all(self) -> List[DomainReview]:
        """Get all reviews"""
        orm_list = self.session.query(ORMReview).all()
        return [self._to_domain(r) for r in orm_list]

    def get_by_tenant(self, tenant_id: str) -> List[DomainReview]:
        """Get all reviews for a tenant"""
        orm_list = self.session.query(ORMReview).filter_by(tenant_id=tenant_id).all()
        return [self._to_domain(r) for r in orm_list]

    def get_by_product(self, product_id: str) -> List[DomainReview]:
        """Get reviews for a product - Note: requires join with order_items"""
        # Not implemented as direct product_id FK doesn't exist in review model
        return []

    def get_by_user(self, user_id: str) -> List[DomainReview]:
        """Get reviews written by a user"""
        orm_list = self.session.query(ORMReview).filter_by(user_id=user_id).all()
        return [self._to_domain(r) for r in orm_list]

    def update(self, review_id: str, review: DomainReview) -> DomainReview:
        """Update review"""
        orm = self.session.query(ORMReview).filter_by(id=review_id).first()
        if orm:
            orm.rating = review.rating
            orm.comment = review.comment
            orm.updated_at = datetime.utcnow()
            self.session.flush()
            return self._to_domain(orm)
        raise ValueError(f"Review with id {review_id} not found")

    def delete(self, review_id: str) -> bool:
        """Delete review"""
        orm = self.session.query(ORMReview).filter_by(id=review_id).first()
        if orm:
            self.session.delete(orm)
            self.session.flush()
            return True
        return False
