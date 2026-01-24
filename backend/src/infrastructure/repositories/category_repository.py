from typing import List, Optional
from sqlalchemy.orm import Session
from ...domain.interfaces.icategory_repository import ICategoryRepository
from ...domain.models.category import Category as DomainCategory
from ...infrastructure.models import Category as ORMCategory

class SQLCategoryRepository(ICategoryRepository):
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
        orm = ORMCategory(
            id=category.id,
            tenant_id=category.tenant_id,
            name=category.name,
            display_order=category.display_order,
            created_at=category.created_at,
            updated_at=category.updated_at
        )
        # Upsert logic if needed, but for now strict insert/update
        self.session.add(orm)
        self.session.flush()
        return category

    def get_by_id(self, id: str) -> Optional[DomainCategory]:
        orm = self.session.query(ORMCategory).filter_by(id=id).first()
        return self._to_domain(orm) if orm else None

    def get_all_by_tenant(self, tenant_id: str) -> List[DomainCategory]:
        orms = self.session.query(ORMCategory).filter_by(tenant_id=tenant_id).order_by(ORMCategory.display_order).all()
        return [self._to_domain(o) for o in orms]
