from pydantic import BaseModel, EmailStr


class TokenData(BaseModel):
    id: str


class Login(BaseModel):
    email: EmailStr
    password: str
