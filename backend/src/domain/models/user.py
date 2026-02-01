from dataclasses import dataclass
from datetime import datetime
from typing import Optional
import uuid
from enum import Enum

class UserRole(str, Enum):
    SYS_ADMIN = "SYS_ADMIN"
    OWNER = "OWNER"
    STAFF = "STAFF"
    CUSTOMER = "CUSTOMER"

@dataclass
class User:
    id: uuid.UUID
    email: str
    password_hash: str
    full_name: Optional[str]
    role: UserRole
    created_at: datetime
    updated_at: datetime

    def check_password(self, plain_password: str) -> bool:
        # Business logic can go here (though verifying hash usually needs lib)
        # We'll leave hash verification to a utility or keep it simple
        pass
