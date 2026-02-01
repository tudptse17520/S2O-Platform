from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from enum import Enum


class UserRoleEnum(str, Enum):
    SYS_ADMIN = "SYS_ADMIN"
    OWNER = "OWNER"
    STAFF = "STAFF"
    CUSTOMER = "CUSTOMER"


class CreateUserRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)
    full_name: Optional[str] = None
    role: UserRoleEnum = UserRoleEnum.CUSTOMER


class UpdateUserRequest(BaseModel):
    full_name: Optional[str] = None
    role: Optional[UserRoleEnum] = None


class ChangeRoleRequest(BaseModel):
    role: UserRoleEnum


class UserResponse(BaseModel):
    id: str
    email: str
    full_name: Optional[str]
    role: str
    created_at: Optional[str]
    updated_at: Optional[str]
