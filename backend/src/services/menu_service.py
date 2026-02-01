import uuid
import datetime
from typing import List, Optional
from ..domain.interfaces.icategory_repository import ICategoryRepository
from ..domain.interfaces.iproduct_repository import IProductRepository
from ..domain.models.category import Category
from ..domain.models.product import Product

class MenuService:
    def __init__(self, category_repo: ICategoryRepository, product_repo: IProductRepository):
        self.category_repo = category_repo
        self.product_repo = product_repo

    def create_category(self, tenant_id: str, name: str, display_order: int) -> Category:
        category = Category(
            id=uuid.uuid4(),
            tenant_id=uuid.UUID(tenant_id),
            name=name,
            display_order=display_order,
            created_at=datetime.datetime.utcnow(),
            updated_at=datetime.datetime.utcnow()
        )
        return self.category_repo.save(category)

    def get_categories(self, tenant_id: str) -> List[Category]:
        return self.category_repo.get_all_by_tenant(tenant_id)

    def create_product(self, tenant_id: str, category_id: str, data: dict) -> Product:
        # Verify category exists and belongs to tenant
        category = self.category_repo.get_by_id(category_id)
        if not category or str(category.tenant_id) != tenant_id:
            raise ValueError("Invalid category")

        product = Product(
            id=uuid.uuid4(),
            tenant_id=uuid.UUID(tenant_id),
            category_id=uuid.UUID(category_id),
            name=data['name'],
            price=data['price'],
            description=data.get('description'),
            is_available=data.get('is_available', True),
            embedding_vector=None, # To be handled by AI service later
            created_at=datetime.datetime.utcnow(),
            updated_at=datetime.datetime.utcnow()
        )
        return self.product_repo.save(product)

    def get_products(self, tenant_id: str, category_id: Optional[str] = None) -> List[Product]:
        if category_id:
            return self.product_repo.get_all_by_category(category_id)
        return self.product_repo.get_all_by_tenant(tenant_id)
