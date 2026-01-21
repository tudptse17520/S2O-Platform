from abc import ABC, abstractmethod
from typing import List, Optional
from domain.models.invoice import Invoice


class IInvoiceRepository(ABC):
    """
    Interface for Invoice Repository
    
    Defines contract for invoice data access operations.
    """
    
    @abstractmethod
    def create(self, invoice: Invoice) -> Invoice:
        """Create a new invoice"""
        pass
    
    @abstractmethod
    def get_by_id(self, invoice_id: str) -> Optional[Invoice]:
        """Get invoice by ID"""
        pass
    
    @abstractmethod
    def get_all(self) -> List[Invoice]:
        """Get all invoices"""
        pass
    
    @abstractmethod
    def get_by_order(self, order_id: str) -> List[Invoice]:
        """Get all invoices for an order (split billing support)"""
        pass
    
    @abstractmethod
    def get_by_tenant(self, tenant_id: str) -> List[Invoice]:
        """Get all invoices for a tenant"""
        pass
    
    @abstractmethod
    def update(self, invoice_id: str, invoice: Invoice) -> Invoice:
        """Update invoice"""
        pass
    
    @abstractmethod
    def delete(self, invoice_id: str) -> bool:
        """Delete invoice"""
        pass
    
    @abstractmethod
    def get_by_status(self, tenant_id: str, status: str) -> List[Invoice]:
        """Get invoices by payment status"""
        pass
