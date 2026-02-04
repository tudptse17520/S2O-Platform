from dataclasses import dataclass
from datetime import datetime
from typing import Optional
import uuid

@dataclass
class StaffProfile:
    id: uuid.UUID
    user_id: uuid.UUID
    tenant_id: uuid.UUID
    branch_id: Optional[uuid.UUID]
    position: Optional[str]
    created_at: datetime
    updated_at: datetime
