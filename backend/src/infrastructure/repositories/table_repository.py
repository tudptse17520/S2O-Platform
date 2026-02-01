from typing import List, Optional
from sqlalchemy.orm import Session
from ...domain.interfaces.itable_repository import ITableRepository
from ...domain.models.table import Table as DomainTable
from ...infrastructure.models import Table as ORMTable, TableStatus as ORMTableStatus


class TableRepository(ITableRepository):
    """SQLAlchemy implementation of ITableRepository"""
    
    def __init__(self, session: Session):
        self.session = session

    def _to_domain(self, orm_table: ORMTable) -> DomainTable:
        """Convert ORM model to domain model"""
        return DomainTable(
            id=str(orm_table.id),
            tenant_id=str(orm_table.tenant_id),
            branch_id=str(orm_table.branch_id),
            name=orm_table.name,
            status=orm_table.status.value if orm_table.status else "AVAILABLE",
            created_at=orm_table.created_at,
            updated_at=orm_table.updated_at
        )

    def _to_orm(self, domain_table: DomainTable) -> ORMTable:
        """Convert domain model to ORM model"""
        return ORMTable(
            id=domain_table.id,
            tenant_id=domain_table.tenant_id,
            branch_id=domain_table.branch_id,
            name=domain_table.name,
            status=ORMTableStatus(domain_table.status) if domain_table.status else ORMTableStatus.AVAILABLE,
            created_at=domain_table.created_at,
            updated_at=domain_table.updated_at
        )

    def create(self, table: DomainTable) -> DomainTable:
        """Create a new table"""
        orm_table = self._to_orm(table)
        self.session.add(orm_table)
        self.session.flush()
        return table

    def get_by_id(self, table_id: str) -> Optional[DomainTable]:
        """Get table by ID"""
        orm_table = self.session.query(ORMTable).filter_by(id=table_id).first()
        if orm_table:
            return self._to_domain(orm_table)
        return None

    def get_all(self) -> List[DomainTable]:
        """Get all tables"""
        orm_tables = self.session.query(ORMTable).all()
        return [self._to_domain(t) for t in orm_tables]

    def get_by_tenant(self, tenant_id: str) -> List[DomainTable]:
        """Get all tables for a tenant"""
        orm_tables = self.session.query(ORMTable).filter_by(tenant_id=tenant_id).all()
        return [self._to_domain(t) for t in orm_tables]

    def get_by_status(self, tenant_id: str, status: str) -> List[DomainTable]:
        """Get tables by status (available/occupied)"""
        orm_tables = self.session.query(ORMTable).filter_by(
            tenant_id=tenant_id,
            status=ORMTableStatus(status)
        ).all()
        return [self._to_domain(t) for t in orm_tables]

    def find_available(self, tenant_id: str, seats: int) -> List[DomainTable]:
        """Find available tables that match seat count"""
        # Note: seats filtering not implemented as ORM model doesn't have seats column
        orm_tables = self.session.query(ORMTable).filter_by(
            tenant_id=tenant_id,
            status=ORMTableStatus.AVAILABLE
        ).all()
        return [self._to_domain(t) for t in orm_tables]

    def get_by_branch(self, branch_id: str) -> List[DomainTable]:
        """Get all tables for a branch"""
        orm_tables = self.session.query(ORMTable).filter_by(branch_id=branch_id).all()
        return [self._to_domain(t) for t in orm_tables]

    def update(self, table_id: str, table: DomainTable) -> DomainTable:
        """Update table"""
        orm_table = self.session.query(ORMTable).filter_by(id=table_id).first()
        if orm_table:
            orm_table.name = table.name
            orm_table.status = ORMTableStatus(table.status) if table.status else orm_table.status
            orm_table.updated_at = table.updated_at
            self.session.flush()
            return self._to_domain(orm_table)
        raise ValueError(f"Table with id {table_id} not found")

    def delete(self, table_id: str) -> bool:
        """Delete table"""
        orm_table = self.session.query(ORMTable).filter_by(id=table_id).first()
        if orm_table:
            self.session.delete(orm_table)
            self.session.flush()
            return True
        return False
