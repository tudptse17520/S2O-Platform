from dataclasses import dataclass
from datetime import datetime
from typing import Optional
import uuid

@dataclass
class Category:
    id: uuid.UUID
    tenant_id: uuid.UUID
    name: str
    display_order: int
    created_at: datetime
    updated_at: datetime
