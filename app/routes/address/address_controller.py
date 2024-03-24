from fastapi import APIRouter, Depends, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from app.models.address import Address
from app.models.user import User
from app.utils.oauth2 import get_current_user
from .address_service import AddressService

router = APIRouter(
    prefix="/api/address",
    tags=["Address"]
)

address_service = AddressService()


@router.post("/", status_code=status.HTTP_201_CREATED)
async def add_address(address: Address, current_user=Depends(get_current_user)):
    new_address = await address_service.add_address(address=address)
    return new_address


@router.get("/{user_id}")
async def get_addresses(user_id: str,  current_user=Depends(get_current_user)):
    addresses = await address_service.get_addresses(user_id)
    return addresses


@router.put('/{user_id}/{address_id}', status_code=status.HTTP_201_CREATED)
async def set_default_address(user_id: str, address_id: str, current_user=Depends(get_current_user)):
    updated_address = await address_service.set_default_address(
        user_id=user_id, address_id=address_id)

    return updated_address


@router.get("/get-default/{user_id}", status_code=status.HTTP_201_CREATED)
async def get_default_address(user_id: str, current_user=Depends(get_current_user)):
    default_address = await address_service.get_default_address(user_id)
    return default_address
