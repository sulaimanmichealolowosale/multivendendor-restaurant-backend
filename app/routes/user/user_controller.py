from fastapi import APIRouter, Depends, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from app.models.user import User
from app.utils.oauth2 import get_current_user
from .user_service import UserService

router = APIRouter(
    prefix="/api/user",
    tags=["User"]
)
user_service = UserService()


@router.get("/")
async def get_users(current_user=Depends(get_current_user)):
    users = await user_service.get_users()
    return users


@router.get("/{id}")
async def get_user(id: str, current_user=Depends(get_current_user)):
    user = await user_service.get_user(id)
    return user


@router.get("/{id}/{otp}")
async def verify_account(id: str, otp: str, current_user=Depends(get_current_user)):
    user = await user_service.verify_account(id=id, otp=otp)
    return user


@router.get("/verify-phone/{id}/{phone}")
async def verify_phone(id: str, phone: str, current_user=Depends(get_current_user)):
    user = await user_service.verify_phone(id=id, phone=phone)
    return user
