from itertools import product
from bson import ObjectId
from app.models.cart import Cart
from app.schemas.schema import individual_cart_serializer, individual_food_serializer, individual_restaurant_serializer, list_serial
from app.utils.messages import is_found, server_error
from app.config.database import motor_db
from fastapi import HTTPException, Response, status


class CartService:

    def __init__(self):
        self.collection_name = motor_db['cart']
        self.food_collection_name = motor_db['food']
        self.restaurant_collection_name = motor_db['restaurant']
        self.count = 0

    async def get_collection_name(self, collection_name: str):
        return motor_db[collection_name.lower()]

    async def add_to_cart(self, cart: Cart):
        try:
            existing_product = await self.collection_name.find_one(
                {
                    "user_id": cart.user_id,
                    "product_id": cart.product_id
                }
            )

            product = await self.food_collection_name.find_one({"_id": ObjectId(cart.product_id)})

            if product == None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Product does not exist")

            total_price = cart.quantity*product['price']
            cart.total_price = total_price

            if existing_product:
                self.count += await self.collection_name.count_documents({"user_id": cart.user_id})

                await self.collection_name.find_one_and_update(
                    {"user_id": cart.user_id, "product_id": cart.product_id},
                    {"$set": {
                        "quantity": cart.quantity,
                        "total_price": cart.total_price
                    }}

                )
                cart_items = await self.collection_name.find(
                    {"user_id": cart.user_id}).to_list(length=None)
                return {"cart items": list_serial(cart_items, individual_cart_serializer), "count": self.count}
            else:
                await self.collection_name.insert_one(cart.model_dump())

                self.count += await self.collection_name.count_documents({"user_id": cart.user_id})

                cart_items = await self.collection_name.find(
                    {"user_id": cart.user_id}).to_list(length=None)
                return {"cart items": list_serial(cart_items, individual_cart_serializer), "count": self.count}
        except Exception as e:
            server_error(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, e=e)

    async def remove_from_cart(self, user_id, cart_id):
        try:
            await self.collection_name.find_one_and_delete({"_id": cart_id})
            self.count = await self.collection_name.count_documents({"user_id": user_id})
            return Response(content={"count": self.count}, status_code=status.HTTP_204_NO_CONTENT)

        except Exception as e:
            server_error(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, e=e)

    async def get_cart(self, user_id):
        try:

            cart_items = await self.collection_name.find({"user_id": user_id}).to_list(length=None)
            cart = []
            for item in cart_items:
                food = await self.food_collection_name.find_one({"_id": ObjectId(item['product_id'])})
                if food is None:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND, detail="No product found")
                restaurant = await self.restaurant_collection_name.find_one({"_id": ObjectId(food['restaurant'])})
                if restaurant is None:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND, detail="No restaurant found")
                cart.append({
                    'id': str(item['_id']),
                    'user_id': user_id,
                    'product_id': item['product_id'],
                    'additives': item['additives'],
                    'total_price': item['total_price'],
                    'quantity': item['quantity'],
                    'created_at': item['created_at'],
                    'product': individual_food_serializer(food),
                    'restaurant': individual_restaurant_serializer(restaurant)
                })

            return cart
        except Exception as e:
            server_error(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, e=e)

    async def decrement_product_qty(self, id):
        try:
            cart_item = await self.collection_name.find_one({"_id": ObjectId(id)})
            if cart_item is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Cart item not found")

            product_price = cart_item['total_price']/cart_item['quantity']
            if cart_item['quantity'] > 1:
                quantity = cart_item['quantity'] - 1
                total_price = cart_item['total_price'] - product_price
                new_cart = await self.collection_name.find_one_and_update(
                    {'_id': ObjectId(id)},
                    {'$set': {
                        'quantity': quantity,
                        'total_price': total_price
                    }}
                )
                new_cart['total_price'] = total_price
                new_cart['quantity'] = quantity
                return individual_cart_serializer(new_cart)
            else:
                await self.collection_name.find_one_and_delete({"_id": ObjectId(id)})
                return Response(content="Successfully deleted", status_code=status.HTTP_204_NO_CONTENT)

        except Exception as e:
            server_error(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, e=e)

    async def get_cart_count(self, user_id: str):
        try:
            cart_count = await self.collection_name.count_documents(
                {"user_id": user_id})
            return {"cart_count": cart_count}
        except Exception as e:
            server_error(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, e=e)
