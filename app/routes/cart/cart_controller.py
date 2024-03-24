from fastapi import APIRouter, Depends, status
from app.models.cart import Cart
from app.utils.oauth2 import get_current_user
from .cart_service import CartService

router = APIRouter(
    prefix="/api/cart",
    tags=["Cart"]
)

cart_service = CartService()


@router.post('/', status_code=status.HTTP_201_CREATED)
async def add_to_cart(cart: Cart,  current_user=Depends(get_current_user)):
    cart_item = await cart_service.add_to_cart(cart)
    return cart_item


@router.get('/{user_id}')
async def get_cart(user_id,  current_user=Depends(get_current_user)):
    cart = await cart_service.get_cart(user_id=user_id)
    return cart


@router.delete('/{user_id}/{cart_id}')
async def remove_from_cart(user_id, cart_id,  current_user=Depends(get_current_user)):
    cart_item = await cart_service.remove_from_cart(user_id=user_id, cart_id=cart_id)
    return cart_item


@router.put('/{id}/')
async def decrement_product_qty(id: str,  current_user=Depends(get_current_user)):
    cart = await cart_service.decrement_product_qty(id=id)
    return cart


@router.get('/{user_id}/')
async def get_cart_count(user_id: str,  current_user=Depends(get_current_user)):
    cart = await cart_service.get_cart_count(user_id=user_id)
    return cart
