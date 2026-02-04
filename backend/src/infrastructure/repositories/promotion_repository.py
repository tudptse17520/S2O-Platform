from typing import List, Optional
from datetime import datetime, date
from sqlalchemy.orm import Session
from ...domain.interfaces.ipromotion_repository import IPromotionRepository
from ...domain.models.promotion import Promotion as DomainPromotion
from ...infrastructure.models import Promotion as ORMPromotion


class PromotionRepository(IPromotionRepository):
    """SQLAlchemy implementation of IPromotionRepository"""
    
    def __init__(self, session: Session):
        self.session = session

    def _to_domain(self, orm_promo: ORMPromotion) -> DomainPromotion:
        """Convert ORM model to domain model"""
        return DomainPromotion(
            id=str(orm_promo.id),
            tenant_id=str(orm_promo.tenant_id),
            code=orm_promo.code,
            promotion_type=orm_promo.type,
            value=orm_promo.value,
            start_date=orm_promo.start_date.date() if orm_promo.start_date else date.today(),
            end_date=orm_promo.end_date.date() if orm_promo.end_date else date.today()
        )

    def _to_orm(self, domain_promo: DomainPromotion) -> ORMPromotion:
        """Convert domain model to ORM model"""
        return ORMPromotion(
            id=domain_promo.id,
            tenant_id=domain_promo.tenant_id,
            code=domain_promo.code,
            type=domain_promo.promotion_type,
            value=domain_promo.value,
            start_date=datetime.combine(domain_promo.start_date, datetime.min.time()),
            end_date=datetime.combine(domain_promo.end_date, datetime.min.time()),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

    def create(self, promotion: DomainPromotion) -> DomainPromotion:
        """Create a new promotion"""
        orm_promo = self._to_orm(promotion)
        self.session.add(orm_promo)
        self.session.flush()
        return promotion

    def get_by_id(self, promotion_id: str) -> Optional[DomainPromotion]:
        """Get promotion by ID"""
        orm = self.session.query(ORMPromotion).filter_by(id=promotion_id).first()
        if orm:
            return self._to_domain(orm)
        return None

    def get_all(self) -> List[DomainPromotion]:
        """Get all promotions"""
        orm_list = self.session.query(ORMPromotion).all()
        return [self._to_domain(p) for p in orm_list]

    def get_by_tenant(self, tenant_id: str) -> List[DomainPromotion]:
        """Get all promotions for a tenant"""
        orm_list = self.session.query(ORMPromotion).filter_by(tenant_id=tenant_id).all()
        return [self._to_domain(p) for p in orm_list]

    def get_by_code(self, tenant_id: str, code: str) -> Optional[DomainPromotion]:
        """Get promotion by code for a tenant"""
        orm = self.session.query(ORMPromotion).filter_by(
            tenant_id=tenant_id,
            code=code
        ).first()
        if orm:
            return self._to_domain(orm)
        return None

    def update(self, promotion_id: str, promotion: DomainPromotion) -> DomainPromotion:
        """Update promotion"""
        orm = self.session.query(ORMPromotion).filter_by(id=promotion_id).first()
        if orm:
            orm.code = promotion.code
            orm.type = promotion.promotion_type
            orm.value = promotion.value
            orm.start_date = datetime.combine(promotion.start_date, datetime.min.time())
            orm.end_date = datetime.combine(promotion.end_date, datetime.min.time())
            orm.updated_at = datetime.utcnow()
            self.session.flush()
            return self._to_domain(orm)
        raise ValueError(f"Promotion with id {promotion_id} not found")

    def delete(self, promotion_id: str) -> bool:
        """Delete promotion"""
        orm = self.session.query(ORMPromotion).filter_by(id=promotion_id).first()
        if orm:
            self.session.delete(orm)
            self.session.flush()
            return True
        return False

    def get_active_promotions(self, tenant_id: str) -> List[DomainPromotion]:
        """Get all active promotions for a tenant"""
        now = datetime.utcnow()
        orm_list = self.session.query(ORMPromotion).filter(
            ORMPromotion.tenant_id == tenant_id,
            ORMPromotion.start_date <= now,
            ORMPromotion.end_date >= now
        ).all()
        return [self._to_domain(p) for p in orm_list]
