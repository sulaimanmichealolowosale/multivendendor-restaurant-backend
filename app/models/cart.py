from datetime import datetime
from typing import Optional
from bson import ObjectId
from pydantic import BaseModel, Field, validator


class Cart (BaseModel):
    user_id: str
    product_id: str
    additives: list[str] = []
    total_price: float
    quantity: int
    created_at: datetime = Field(default_factory=datetime.utcnow)

    @validator("user_id")
    def validate_user_id(cls, value):
        if not ObjectId.is_valid(value) and value == None:
            raise ValueError("Invalid user_id")
        return value

    @validator("product_id")
    def validate_product_id(cls, value):
        if not ObjectId.is_valid(value) and value == None:
            raise ValueError("Invalid product_id")
        return value
