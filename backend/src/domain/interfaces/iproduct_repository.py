from abc import ABC, abstractmethod
from typing import List, Optional
from ..models.product import Product

class IProductRepository(ABC):
    @abstractmethod
    def save(self, product: Product) -> Product:
        pass

    @abstractmethod
    def get_by_id(self, id: str) -> Optional[Product]:
        pass

    @abstractmethod
    def get_all_by_category(self, category_id: str) -> List[Product]:
        pass

    @abstractmethod
    def get_all_by_tenant(self, tenant_id: str) -> List[Product]:
        pass
