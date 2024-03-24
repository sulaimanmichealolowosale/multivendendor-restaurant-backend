from datetime import datetime
from pydantic import BaseModel, Field, conint
#


class Coordinate(BaseModel):
    id: str
    longitude: float
    latitude: float
    latitude_delta: float
    longitude_delta: float
    address: str
    title: str


class Restaurant(BaseModel):
    title: str = Field(..., min_length=3, max_length=50, strict=True)
    time: str = Field(..., min_length=3, max_length=50)
    image_url: str
    foods: list = Field(min_length=1, default_factory=lambda: [])
    pickup: bool = True
    delivery: bool = True
    is_available: bool = True
    owner: str = Field(..., min_length=1, max_length=50)
    code: str = Field(..., min_length=1)
    logo_url: str
    rating: int = Field(gt=0, lt=6)
    rating_count: str = "167"
    verification: str = Field(..., default_factory=lambda: "Pending", examples=[
                              "Pending", "Verified", "Rejected"])
    verification_message: str = "Your restaurant is under rewiew. We will notify you once it is verfied."
    coords: Coordinate
    created_at: datetime = Field(default_factory=datetime.utcnow)
