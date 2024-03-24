from datetime import datetime
from enum import Enum
from bson import ObjectId
from pydantic import BaseModel, Field, validator


class RatingEnum(Enum):
    restaurant = "Restaurant"
    driver = "Driver"
    food = "Food"


class Rating(BaseModel):
    user_id: str = Field(..., min_length=4, max_length=50)
    rating: int = Field(ge=1, le=5)
    rating_type: str
    product_id: str = Field(..., min_length=1, max_length=50)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    @validator("rating_type")
    def validate_rating_type(cls, value):
        if (value != RatingEnum.restaurant.value) and (value != RatingEnum.driver.value) and (value != RatingEnum.food.value):
            raise ValueError("Invalid Rating Type")
        return value

    @validator("product_id")
    def validate_product_id(cls, value):
        if not ObjectId.is_valid(value):
            raise ValueError("Invalid ObjectId")
        return value
