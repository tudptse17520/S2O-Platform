from pydantic import BaseModel, Field
from typing import Optional, List
from uuid import UUID


class CreateOrderRequest(BaseModel):
    branch_id: str
    table_id: Optional[str] = None
    customer_id: Optional[str] = None
    note: Optional[str] = None


class UpdateOrderStatusRequest(BaseModel):
    status: str = Field(..., description="Order status: PENDING, CONFIRMED, PREPARING, READY, SERVED, COMPLETED, CANCELLED")


class AddOrderItemRequest(BaseModel):
    product_id: str
    quantity: int = Field(1, ge=1)
    price: float = Field(..., gt=0)


class OrderItemResponse(BaseModel):
    id: str
    order_id: str
    product_id: str
    quantity: int
    price_at_order: float
    subtotal: float
    item_status: str


class OrderResponse(BaseModel):
    id: str
    tenant_id: str
    branch_id: str
    table_id: Optional[str] = None
    customer_id: Optional[str] = None
    status: str
    total_amount: float
    note: Optional[str] = None
    items: Optional[List[OrderItemResponse]] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
