from pydantic import BaseModel, Field
from typing import Optional


class CreateTableRequest(BaseModel):
    branch_id: str
    name: str = Field(..., min_length=1, max_length=50)


class UpdateTableRequest(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=50)


class UpdateTableStatusRequest(BaseModel):
    status: str = Field(..., description="Table status: AVAILABLE, OCCUPIED")


class TableResponse(BaseModel):
    id: str
    tenant_id: str
    branch_id: str
    name: str
    status: str
    qr_code_link: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
