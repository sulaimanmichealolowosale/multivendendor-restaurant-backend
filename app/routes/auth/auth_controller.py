from fastapi import APIRouter, Depends, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from app.models.auth import Login
from app.models.user import User
from .auth_service import AuthService

router = APIRouter(
    prefix="/api/auth",
    tags=["Auth"]
)
auth_service = AuthService()


@router.post('/register', status_code=status.HTTP_201_CREATED)
async def register(user: User):
    new_user = await auth_service.register(user=user)
    return new_user


@router.post('/login')
async def login(response: Response, login_details: Login):
    user = await auth_service.login(
        login_details=login_details, response=response)
    return user


@router.get('/logout')
async def logout(response: Response):
    user = await auth_service.logout(response=response)
    return user
