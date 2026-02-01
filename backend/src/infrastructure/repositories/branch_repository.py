from typing import List, Optional
from sqlalchemy.orm import Session
from ...domain.interfaces.ibranch_repository import IBranchRepository
from ...domain.models.branch import Branch as DomainBranch
from ...infrastructure.models import Branch as ORMBranch


class BranchRepository(IBranchRepository):
    """SQLAlchemy implementation of IBranchRepository"""
    
    def __init__(self, session: Session):
        self.session = session

    def _to_domain(self, orm_branch: ORMBranch) -> DomainBranch:
        """Convert ORM model to domain model"""
        return DomainBranch(
            id=str(orm_branch.id),
            tenant_id=str(orm_branch.tenant_id),
            name=orm_branch.name,
            address=orm_branch.address,
            is_active=orm_branch.is_active,
            created_at=orm_branch.created_at,
            updated_at=orm_branch.updated_at
        )

    def _to_orm(self, domain_branch: DomainBranch) -> ORMBranch:
        """Convert domain model to ORM model"""
        return ORMBranch(
            id=domain_branch.id,
            tenant_id=domain_branch.tenant_id,
            name=domain_branch.name,
            address=domain_branch.address,
            is_active=domain_branch.is_active,
            created_at=domain_branch.created_at,
            updated_at=domain_branch.updated_at
        )

    def create(self, branch: DomainBranch) -> DomainBranch:
        """Create a new branch"""
        orm_branch = self._to_orm(branch)
        self.session.add(orm_branch)
        self.session.flush()
        return branch

    def get_by_id(self, branch_id: str) -> Optional[DomainBranch]:
        """Get branch by ID"""
        orm_branch = self.session.query(ORMBranch).filter_by(id=branch_id).first()
        if orm_branch:
            return self._to_domain(orm_branch)
        return None

    def get_all(self) -> List[DomainBranch]:
        """Get all branches"""
        orm_branches = self.session.query(ORMBranch).all()
        return [self._to_domain(b) for b in orm_branches]

    def get_by_tenant(self, tenant_id: str) -> List[DomainBranch]:
        """Get all branches for a tenant"""
        orm_branches = self.session.query(ORMBranch).filter_by(tenant_id=tenant_id).all()
        return [self._to_domain(b) for b in orm_branches]

    def update(self, branch_id: str, branch: DomainBranch) -> DomainBranch:
        """Update branch"""
        orm_branch = self.session.query(ORMBranch).filter_by(id=branch_id).first()
        if orm_branch:
            orm_branch.name = branch.name
            orm_branch.address = branch.address
            orm_branch.is_active = branch.is_active
            orm_branch.updated_at = branch.updated_at
            self.session.flush()
            return self._to_domain(orm_branch)
        raise ValueError(f"Branch with id {branch_id} not found")

    def delete(self, branch_id: str) -> bool:
        """Delete branch"""
        orm_branch = self.session.query(ORMBranch).filter_by(id=branch_id).first()
        if orm_branch:
            self.session.delete(orm_branch)
            self.session.flush()
            return True
        return False

    def get_by_name(self, tenant_id: str, name: str) -> Optional[DomainBranch]:
        """Find branch by name within a tenant"""
        orm_branch = self.session.query(ORMBranch).filter_by(
            tenant_id=tenant_id, name=name
        ).first()
        if orm_branch:
            return self._to_domain(orm_branch)
        return None
