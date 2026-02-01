import uuid
from datetime import datetime
from typing import List, Optional, Dict, Any

from ..domain.interfaces.itenant_repository import ITenantRepository
from ..domain.models.tenant import Tenant


class TenantService:
    """Service layer for Tenant operations"""
    
    def __init__(self, tenant_repo: ITenantRepository):
        self.tenant_repo = tenant_repo

    def create_tenant(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new tenant"""
        tenant_id = uuid.uuid4()
        slug = data['name'].lower().replace(' ', '-') + '-' + str(uuid.uuid4())[:8]
        
        tenant = Tenant(
            id=tenant_id,
            name=data['name'],
            slug=slug,
            subscription_plan=data.get('subscription_plan', 'FREE'),
            is_active=data.get('is_active', True),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        saved_tenant = self.tenant_repo.save(tenant)
        return self._to_dict(saved_tenant)

    def get_tenant(self, tenant_id: str) -> Optional[Dict[str, Any]]:
        """Get a tenant by ID"""
        tenant = self.tenant_repo.get_by_id(tenant_id)
        if tenant:
            return self._to_dict(tenant)
        return None

    def get_all_tenants(self) -> List[Dict[str, Any]]:
        """Get all tenants"""
        tenants = self.tenant_repo.get_all()
        return [self._to_dict(t) for t in tenants]

    def update_tenant(self, tenant_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update a tenant"""
        existing = self.tenant_repo.get_by_id(tenant_id)
        if not existing:
            raise ValueError(f"Tenant with id {tenant_id} not found")
        
        if 'name' in data:
            existing.name = data['name']
        if 'subscription_plan' in data:
            existing.subscription_plan = data['subscription_plan']
        if 'is_active' in data:
            existing.is_active = data['is_active']
        existing.updated_at = datetime.utcnow()
        
        updated_tenant = self.tenant_repo.update(tenant_id, existing)
        return self._to_dict(updated_tenant)

    def deactivate_tenant(self, tenant_id: str) -> Dict[str, Any]:
        """Deactivate a tenant"""
        existing = self.tenant_repo.get_by_id(tenant_id)
        if not existing:
            raise ValueError(f"Tenant with id {tenant_id} not found")
        
        existing.is_active = False
        existing.updated_at = datetime.utcnow()
        
        updated_tenant = self.tenant_repo.update(tenant_id, existing)
        return self._to_dict(updated_tenant)

    def _to_dict(self, tenant: Tenant) -> Dict[str, Any]:
        """Convert tenant entity to dictionary"""
        return {
            "id": str(tenant.id),
            "name": tenant.name,
            "slug": tenant.slug,
            "subscription_plan": tenant.subscription_plan,
            "is_active": tenant.is_active,
            "created_at": tenant.created_at.isoformat() if tenant.created_at else None,
            "updated_at": tenant.updated_at.isoformat() if tenant.updated_at else None
        }
