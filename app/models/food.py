from datetime import datetime
from typing import Any, List
from bson import ObjectId
from pydantic import BaseModel, Field, validator


class Additives(BaseModel):
    id: int
    title: str
    price: str


class Food(BaseModel):
    title: str = Field(..., min_length=3, max_length=50)
    time: str = Field(..., min_length=3, max_length=50)
    food_tags: list
    food_type: list
    category: str = Field(..., min_length=1, max_length=50)
    code: str = Field(..., min_length=1, max_length=50)
    is_available: bool = True
    restaurant: str
    rating: float = 3
    rating_count: str = "267"
    description: str = Field(min_length=1)
    price: float = Field(gt=0)
    additives: List[Additives] = []
    image_urls: List[str]
    created_at: datetime = Field(default_factory=datetime.utcnow)

    @validator("restaurant")
    def validate_restaurant(cls, value):
        if not ObjectId.is_valid(value):
            raise ValueError("Invalid ObjectId")
        return value


# [
#   {
#     "title": "Tiramisu",
#     "food_tags": ["Italian", "Dessert", "Coffee", "Mascarpone", "Cocoa"],
#     "food_type": ["Dessert"],
#     "code": "41007428",
#     "is_available": true,
#     "restaurant": "65ef7f0235f2ca481ee93cbc",
#     "rating": 4.9,
#     "rating_count": "420",
#     "description":
#         "A classic Italian dessert made of layers of coffee-soaked ladyfingers and creamy mascarpone, topped with cocoa.",
#     "price": 7.99,
#     "additives": [
#       {"id": 1, "title": "Ladyfingers", "price": "1.00"},
#       {"id": 2, "title": "Coffee", "price": "1.50"},
#       {"id": 3, "title": "Mascarpone Cheese", "price": "2.50"},
#       {"id": 4, "title": "Cocoa", "price": "0.50"},
#       {"id": 5, "title": "Sugar", "price": "0.50"}
#     ],
#     "image_url":
#       "https://d326fntlu7tb1e.cloudfront.net/uploads/5c2a9ca8-eb07-400b-b8a6-2acfab2a9ee2-image001.webp",
#     "category": "65ef6b2501b9b5f3bf3ffe6c",
#     "time": "35 min",
#     "created_at": "2024-03-11T22:18:38.483Z"
#   },
# ]
