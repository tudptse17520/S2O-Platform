import uuid
from datetime import datetime
from typing import List, Optional, Dict, Any

from ..domain.interfaces.itable_repository import ITableRepository
from ..domain.models.table import Table, TableStatus


class TableService:
    """Service layer for Table operations"""
    
    def __init__(self, table_repo: ITableRepository):
        self.table_repo = table_repo

    def create_table(self, tenant_id: str, branch_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new table"""
        table_id = uuid.uuid4()
        table = Table(
            id=str(table_id),
            tenant_id=tenant_id,
            branch_id=branch_id,
            name=data['name'],
            status=TableStatus.AVAILABLE,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        saved_table = self.table_repo.create(table)
        return self._to_dict(saved_table)

    def get_table(self, table_id: str) -> Optional[Dict[str, Any]]:
        """Get a table by ID"""
        table = self.table_repo.get_by_id(table_id)
        if table:
            return self._to_dict(table)
        return None

    def get_tables_by_tenant(self, tenant_id: str) -> List[Dict[str, Any]]:
        """Get all tables for a tenant"""
        tables = self.table_repo.get_by_tenant(tenant_id)
        return [self._to_dict(t) for t in tables]

    def get_tables_by_branch(self, branch_id: str) -> List[Dict[str, Any]]:
        """Get all tables for a branch"""
        tables = self.table_repo.get_by_branch(branch_id)
        return [self._to_dict(t) for t in tables]

    def get_available_tables(self, tenant_id: str) -> List[Dict[str, Any]]:
        """Get all available tables for a tenant"""
        tables = self.table_repo.get_by_status(tenant_id, TableStatus.AVAILABLE.value)
        return [self._to_dict(t) for t in tables]

    def update_table(self, table_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update a table"""
        existing = self.table_repo.get_by_id(table_id)
        if not existing:
            raise ValueError(f"Table with id {table_id} not found")
        
        existing.name = data.get('name', existing.name)
        existing.updated_at = datetime.utcnow()
        
        updated_table = self.table_repo.update(table_id, existing)
        return self._to_dict(updated_table)

    def update_table_status(self, table_id: str, status: str) -> Dict[str, Any]:
        """Update table status"""
        existing = self.table_repo.get_by_id(table_id)
        if not existing:
            raise ValueError(f"Table with id {table_id} not found")
        
        existing.status = status
        existing.updated_at = datetime.utcnow()
        
        updated_table = self.table_repo.update(table_id, existing)
        return self._to_dict(updated_table)

    def delete_table(self, table_id: str) -> bool:
        """Delete a table"""
        return self.table_repo.delete(table_id)

    def generate_qr_code(self, table_id: str, base_url: str) -> str:
        """Generate QR code URL for a table"""
        table = self.table_repo.get_by_id(table_id)
        if not table:
            raise ValueError(f"Table with id {table_id} not found")
        
        # QR code URL pattern: {base_url}/menu?table={table_id}&tenant={tenant_id}
        qr_url = f"{base_url}/menu?table={table_id}&tenant={table.tenant_id}"
        return qr_url

    def _to_dict(self, table: Table) -> Dict[str, Any]:
        """Convert table entity to dictionary"""
        return {
            "id": str(table.id),
            "tenant_id": str(table.tenant_id),
            "branch_id": str(table.branch_id),
            "name": table.name,
            "status": table.status if isinstance(table.status, str) else table.status.value,
            "qr_code_link": table.qr_code_link,
            "created_at": table.created_at.isoformat() if table.created_at else None,
            "updated_at": table.updated_at.isoformat() if table.updated_at else None
        }
