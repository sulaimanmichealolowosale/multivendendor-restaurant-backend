from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class Address (BaseModel):
    user_id: str = Field(..., min_length=4, max_length=50)
    address_line_1: str = Field(..., min_length=3, max_length=50)
    postal_code: str = Field(..., min_length=3, max_length=50)
    default: bool = False
    delivery_instructions: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]
    created_at: datetime = Field(default_factory=datetime.utcnow)
