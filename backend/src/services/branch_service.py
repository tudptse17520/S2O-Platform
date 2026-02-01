import uuid
from datetime import datetime
from typing import List, Optional, Dict, Any

from ..domain.interfaces.ibranch_repository import IBranchRepository
from ..domain.models.branch import Branch


class BranchService:
    """Service layer for Branch operations"""
    
    def __init__(self, branch_repo: IBranchRepository):
        self.branch_repo = branch_repo

    def create_branch(self, tenant_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new branch for a tenant"""
        branch_id = uuid.uuid4()
        branch = Branch(
            id=str(branch_id),
            tenant_id=tenant_id,
            name=data['name'],
            address=data.get('address'),
            is_active=data.get('is_active', True),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        saved_branch = self.branch_repo.create(branch)
        return self._to_dict(saved_branch)

    def get_branch(self, branch_id: str) -> Optional[Dict[str, Any]]:
        """Get a branch by ID"""
        branch = self.branch_repo.get_by_id(branch_id)
        if branch:
            return self._to_dict(branch)
        return None

    def get_branches_by_tenant(self, tenant_id: str) -> List[Dict[str, Any]]:
        """Get all branches for a tenant"""
        branches = self.branch_repo.get_by_tenant(tenant_id)
        return [self._to_dict(b) for b in branches]

    def update_branch(self, branch_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update a branch"""
        existing = self.branch_repo.get_by_id(branch_id)
        if not existing:
            raise ValueError(f"Branch with id {branch_id} not found")
        
        existing.name = data.get('name', existing.name)
        existing.address = data.get('address', existing.address)
        existing.is_active = data.get('is_active', existing.is_active)
        existing.updated_at = datetime.utcnow()
        
        updated_branch = self.branch_repo.update(branch_id, existing)
        return self._to_dict(updated_branch)

    def delete_branch(self, branch_id: str) -> bool:
        """Delete a branch"""
        return self.branch_repo.delete(branch_id)

    def _to_dict(self, branch: Branch) -> Dict[str, Any]:
        """Convert branch entity to dictionary"""
        return {
            "id": str(branch.id),
            "tenant_id": str(branch.tenant_id),
            "name": branch.name,
            "address": branch.address,
            "is_active": branch.is_active,
            "created_at": branch.created_at.isoformat() if branch.created_at else None,
            "updated_at": branch.updated_at.isoformat() if branch.updated_at else None
        }
