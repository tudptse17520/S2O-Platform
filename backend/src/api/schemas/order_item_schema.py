from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


class OrderItemStatusEnum(str, Enum):
    PENDING = "PENDING"
    COOKING = "COOKING"
    PREPARING = "PREPARING"
    READY = "READY"
    SERVED = "SERVED"
    CANCELLED = "CANCELLED"


class CreateOrderItemRequest(BaseModel):
    order_id: str = Field(..., description="Order ID")
    product_id: str = Field(..., description="Product ID")
    quantity: int = Field(..., ge=1, description="Quantity")
    price_at_order: float = Field(..., gt=0, description="Price at time of order")
    item_status: Optional[OrderItemStatusEnum] = Field(default=OrderItemStatusEnum.PENDING)


class UpdateOrderItemRequest(BaseModel):
    quantity: Optional[int] = Field(None, ge=1)
    item_status: Optional[OrderItemStatusEnum] = None


class UpdateOrderItemStatusRequest(BaseModel):
    item_status: OrderItemStatusEnum


class OrderItemResponse(BaseModel):
    id: str
    tenant_id: str
    order_id: str
    product_id: str
    quantity: int
    price_at_order: float
    item_status: str
    subtotal: float
