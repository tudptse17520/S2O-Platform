from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Any
import uuid

@dataclass
class Product:
    id: uuid.UUID
    tenant_id: uuid.UUID
    category_id: uuid.UUID
    name: str
    price: float
    description: Optional[str]
    is_available: bool
    embedding_vector: Optional[Any] # pgvector
    created_at: datetime
    updated_at: datetime
