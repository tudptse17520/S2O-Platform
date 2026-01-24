from dataclasses import dataclass
from datetime import datetime
import uuid

@dataclass
class Tenant:
    id: uuid.UUID
    name: str
    slug: str
    subscription_plan: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
