from typing import List, Optional, Dict, Any
import uuid
from datetime import datetime

from ..domain.interfaces.icategory_repository import ICategoryRepository
from ..domain.models.category import Category


class CategoryService:
    """Service for category-related business logic"""
    
    def __init__(self, category_repo: ICategoryRepository):
        self.category_repo = category_repo
    
    def create_category(self, tenant_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new category"""
        category = Category(
            id=uuid.uuid4(),
            tenant_id=uuid.UUID(tenant_id),
            name=data['name'],
            display_order=data.get('display_order', 0),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        created = self.category_repo.save(category)
        return self._to_dict(created)
    
    def get_category(self, category_id: str) -> Optional[Dict[str, Any]]:
        """Get category by ID"""
        category = self.category_repo.get_by_id(category_id)
        return self._to_dict(category) if category else None
    
    def get_categories_by_tenant(self, tenant_id: str) -> List[Dict[str, Any]]:
        """Get all categories for a tenant"""
        categories = self.category_repo.get_all_by_tenant(tenant_id)
        return [self._to_dict(c) for c in categories]
    
    def update_category(self, category_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update category"""
        category = self.category_repo.get_by_id(category_id)
        if not category:
            raise ValueError(f"Category {category_id} not found")
        
        if 'name' in data and data['name'] is not None:
            category.name = data['name']
        if 'display_order' in data and data['display_order'] is not None:
            category.display_order = data['display_order']
        
        category.updated_at = datetime.utcnow()
        
        updated = self.category_repo.save(category)
        return self._to_dict(updated)
    
    def delete_category(self, category_id: str) -> bool:
        """Delete category"""
        return self.category_repo.delete(category_id)
    
    def reorder_categories(self, tenant_id: str, order: List[str]) -> List[Dict[str, Any]]:
        """Reorder categories by list of IDs"""
        categories = self.category_repo.get_all_by_tenant(tenant_id)
        category_map = {str(c.id): c for c in categories}
        
        for index, cat_id in enumerate(order):
            if cat_id in category_map:
                category_map[cat_id].display_order = index
                category_map[cat_id].updated_at = datetime.utcnow()
                self.category_repo.save(category_map[cat_id])
        
        return self.get_categories_by_tenant(tenant_id)
    
    def _to_dict(self, category: Category) -> Dict[str, Any]:
        return {
            "id": str(category.id),
            "tenant_id": str(category.tenant_id),
            "name": category.name,
            "display_order": category.display_order,
            "created_at": category.created_at.isoformat() if category.created_at else None,
            "updated_at": category.updated_at.isoformat() if category.updated_at else None,
        }
