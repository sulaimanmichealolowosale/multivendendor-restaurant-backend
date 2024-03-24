from itertools import product
from app.models.cart import Cart
from app.models.order import Order
from app.schemas.schema import individual_order_serializer, list_serial
from app.utils.messages import is_found, server_error
from app.config.database import motor_db
from fastapi import HTTPException, Response, status


class OrderService:

    def __init__(self):
        self.collection_name = motor_db['order']
        self.food_collection_name = motor_db['food']
        self.restaurant_collection_name = motor_db['restaurant']
        self.cart_collection_name = motor_db['cart']

    async def place_order(self, user_id, order: Order):
        try:
            order.user_id = user_id
            await self.collection_name.insert_one(order.model_dump())
            return {"Message": "Order placed successful"}
        except Exception as e:
            server_error(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, e=e)

    async def get_orders(self, user_id):
        try:
            orders = await self.collection_name.find({"user_id": user_id}).to_list(length=None)
            return list_serial(orders, individual_order_serializer)
        except Exception as e:
            print(e)
