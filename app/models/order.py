from datetime import datetime
from enum import Enum
from typing import Optional
from bson import ObjectId
from pydantic import BaseModel, Field, validator


class OrderItem (BaseModel):
    food_id: str
    quantity: int = 1
    price: int
    additives: list[str] = []
    instructions: str = ''

    @validator("food_id")
    def validate_food_id(cls, value):
        if not ObjectId.is_valid(value) and value == None:
            raise ValueError("Invalid food_id")
        return value


class PaymentStatusEnum(Enum):
    pending = "pending"
    completed = "completed"
    failed = "failed"


class OrderStatusEnum(Enum):
    pending = "pending"
    placed = "placed"
    preparing = "preparing"
    manual = "manual"
    delivered = "delivered"
    canceled = "canceled"
    ready = "ready"
    out_for_delivery = "out_for_delivery"


class Order (BaseModel):
    user_id: str
    order_items: list[OrderItem]
    order_total: int
    delivery_fee: int
    grand_total: int
    delivery_address_id: str
    restsaurant_address: str
    payment_method: str
    payment_status: str = PaymentStatusEnum.pending.value
    order_status: str = "pending"
    restaurant_id: str
    restaurrant_coords: int
    reciepient_coords: int
    driver_id: str = ''
    rating: int = 3
    feedback: str = ''
    promo_code: str = ''
    discount_amount: int
    notes: str = ''
    created_at: datetime = Field(default_factory=datetime.utcnow)

    @validator("user_id", "delivery_address_id", "restaurant_id")
    def validate_objectid_field(cls, value):
        if not ObjectId.is_valid(value) and value == None:
            raise ValueError("Invalid user_id")
        return value

    @validator("order_status")
    def validate_order_status(cls, value):
        if (value != OrderStatusEnum.canceled.value) and (value != OrderStatusEnum.delivered.value) and (value != OrderStatusEnum.manual.value) and (value != OrderStatusEnum.out_for_delivery.value) and (value != OrderStatusEnum.placed.value) and (value != OrderStatusEnum.preparing.value) and (value != OrderStatusEnum.ready.value) and (value != OrderStatusEnum.pending.value):
            raise ValueError("Invalid Order Status")
        return value

    @validator("payment_status")
    def validate_payment_status(cls, value):
        if (value != PaymentStatusEnum.completed.value) and (value != PaymentStatusEnum.failed.value) and (value != PaymentStatusEnum.pending.value):
            raise ValueError("Invalid Payment Status")
        return value
