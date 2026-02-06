from typing import List, Optional
import uuid
from sqlalchemy.orm import Session
from ...domain.interfaces.icategory_repository import ICategoryRepository
from ...domain.models.category import Category as DomainCategory
from ...infrastructure.models import Category as ORMCategory

class CategoryRepository(ICategoryRepository):
    def __init__(self, session: Session):
        self.session = session

    def _to_domain(self, orm: ORMCategory) -> DomainCategory:
        return DomainCategory(
            id=orm.id,
            tenant_id=orm.tenant_id,
            name=orm.name,
            display_order=orm.display_order,
            created_at=orm.created_at,
            updated_at=orm.updated_at
        )

    def save(self, category: DomainCategory) -> DomainCategory:
        # Check if category exists
        existing = self.session.query(ORMCategory).filter_by(id=category.id).first()
        
        if existing:
            # Update existing
            existing.name = category.name
            existing.display_order = category.display_order
            existing.updated_at = category.updated_at
            self.session.flush()
            return category
        else:
            # Create new
            orm = ORMCategory(
                id=category.id,
                tenant_id=category.tenant_id,
                name=category.name,
                display_order=category.display_order,
                created_at=category.created_at,
                updated_at=category.updated_at
            )
            self.session.add(orm)
            self.session.flush()
            return category

    def get_by_id(self, id: str) -> Optional[DomainCategory]:
        uid = uuid.UUID(id) if isinstance(id, str) else id
        orm = self.session.query(ORMCategory).filter_by(id=uid).first()
        return self._to_domain(orm) if orm else None

    def get_all_by_tenant(self, tenant_id: str) -> List[DomainCategory]:
        tid = uuid.UUID(tenant_id) if isinstance(tenant_id, str) else tenant_id
        orms = self.session.query(ORMCategory).filter_by(tenant_id=tid).order_by(ORMCategory.display_order).all()
        return [self._to_domain(o) for o in orms]

    def delete(self, category_id: str) -> bool:
        """Delete category by ID"""
        uid = uuid.UUID(category_id) if isinstance(category_id, str) else category_id
        orm = self.session.query(ORMCategory).filter_by(id=uid).first()
        if orm:
            self.session.delete(orm)
            self.session.flush()
            return True
        return False
