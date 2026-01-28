from typing import List, Optional
from sqlalchemy.orm import Session
from ...domain.interfaces.iproduct_repository import IProductRepository
from ...domain.models.product import Product as DomainProduct
from ...infrastructure.models import Product as ORMProduct

class ProductRepository(IProductRepository):
    def __init__(self, session: Session):
        self.session = session

    def _to_domain(self, orm: ORMProduct) -> DomainProduct:
        return DomainProduct(
            id=orm.id,
            tenant_id=orm.tenant_id,
            category_id=orm.category_id,
            name=orm.name,
            price=orm.price,
            description=orm.description,
            is_available=orm.is_available,
            embedding_vector=orm.embedding_vector,
            created_at=orm.created_at,
            updated_at=orm.updated_at
        )

    def save(self, product: DomainProduct) -> DomainProduct:
        orm = ORMProduct(
            id=product.id,
            tenant_id=product.tenant_id,
            category_id=product.category_id,
            name=product.name,
            price=product.price,
            description=product.description,
            is_available=product.is_available,
            embedding_vector=product.embedding_vector,
            created_at=product.created_at,
            updated_at=product.updated_at
        )
        self.session.add(orm)
        self.session.flush()
        return product

    def get_by_id(self, id: str) -> Optional[DomainProduct]:
        orm = self.session.query(ORMProduct).filter_by(id=id).first()
        return self._to_domain(orm) if orm else None

    def get_all_by_category(self, category_id: str) -> List[DomainProduct]:
        orms = self.session.query(ORMProduct).filter_by(category_id=category_id).all()
        return [self._to_domain(o) for o in orms]

    def get_all_by_tenant(self, tenant_id: str) -> List[DomainProduct]:
        orms = self.session.query(ORMProduct).filter_by(tenant_id=tenant_id).all()
        return [self._to_domain(o) for o in orms]
