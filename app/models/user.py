from datetime import datetime
from enum import Enum
from typing import Optional
from bson import ObjectId
from pydantic import BaseModel, Field, EmailStr, validator


class UserTypeEnum(Enum):
    client = "Client"
    admin = "Admin"
    vendor = "Vendor"
    driver = "Driver"


class User (BaseModel):
    username: str = Field(..., min_length=4, max_length=50)
    email: EmailStr
    otp: str = "none"
    password: str = Field(..., min_length=8, max_length=50)
    phone: str = "0123456789"
    verification: bool = False
    phone_verification: bool = False
    address: Optional[str]
    user_type: str = UserTypeEnum.client.value
    profile: str = "https://raw.githubusercontent.com/sulaimanmichealolowosale/student_housing/main/user_media/image.jpg"
    created_at: datetime = Field(default_factory=datetime.utcnow)

    @validator("address")
    def validate_address(cls, value):
        if not ObjectId.is_valid(value) and value == None:
            raise ValueError("Invalid ObjectId")
        return value
