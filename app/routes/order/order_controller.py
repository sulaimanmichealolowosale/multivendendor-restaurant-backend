from fastapi import APIRouter, Depends, status
from app.models.cart import Cart
from app.models.order import Order
from app.utils.oauth2 import get_current_user
from .order_service import OrderService

router = APIRouter(
    prefix="/api/order",
    tags=["Order"]
)

order_service = OrderService()


@router.post('/{user_id}', status_code=status.HTTP_201_CREATED)
async def place_order(user_id: str, order: Order):
    new_order = await order_service.place_order(user_id=user_id, order=order)
    return new_order


@router.get('/{user_id}')
async def get_order(user_id):
    order = await order_service.get_orders(user_id=user_id)
    return order
