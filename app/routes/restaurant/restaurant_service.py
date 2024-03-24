from typing import List
from bson import ObjectId
from app.models.restaurant import Restaurant
from app.schemas.schema import list_serial, individual_restaurant_serializer
from app.utils.messages import is_found, server_error
from app.config.database import motor_db
from fastapi import status, HTTPException


class RestaurantService:

    def __init__(self):
        self.collection_name = motor_db['restaurant']

    async def insert_many_restaurants(self, restaurants: List[Restaurant]):
        try:
            await self.collection_name.insert_many([restaurant.model_dump() for restaurant in restaurants])
            return {"Message": "Restaurants Inserted successfully"}
        except Exception as e:
            print(e)

    async def insert_restaurant(self, restaurant: Restaurant):
        try:
            existing_restaurant = await self.collection_name.find_one({"title": restaurant.title})
            if existing_restaurant:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f'''A restaurant with title {
                                    restaurant.title} already exists''')
            new_restaurant = await self.collection_name.insert_one(restaurant.model_dump())
            inserted_restaurant = await self.collection_name.find_one({"_id": new_restaurant.inserted_id})
            return individual_restaurant_serializer(inserted_restaurant)

        except Exception as e:
            server_error(status.HTTP_500_INTERNAL_SERVER_ERROR, e)

    async def fetch_all_restaurants(self, code):
        try:
            cursor = self.collection_name.aggregate([
                {"$match": {"code": code}},
            ])
            restaurants = await cursor.to_list(length=None)
            if len(restaurants) < 1:
                cursor = self.collection_name.find()
                restaurants = await cursor.to_list(length=None)
            return list_serial(restaurants, individual_restaurant_serializer)
        except Exception as e:
            server_error(status.HTTP_404_NOT_FOUND, e)

    async def fetch_single_restaurant(self, restaurant_id):
        try:
            restaurant = await self.collection_name.find_one(
                {"_id": ObjectId(restaurant_id)}
            )

            return individual_restaurant_serializer(restaurant)
        except Exception as e:
            server_error(status.HTTP_404_NOT_FOUND, e)

    async def fetch_nearby_restaurants(self, code):
        try:
            restaurants = []
            cursor = self.collection_name.aggregate([
                {"$match": {"code": code, "is_available": True}},
                {"$sample": {"size": 5}}
            ])
            restaurants = await cursor.to_list(length=None)

            if len(restaurants) == 0:
                cursor = self.collection_name.aggregate([
                    {"$match": {"is_available": True}},
                    {"$sample": {"size": 5}}
                ])
                restaurants = await cursor.to_list(length=None)

            # is_found(restaurants)

            return list_serial(restaurants, individual_restaurant_serializer)

        except Exception as e:
            server_error(status.HTTP_404_NOT_FOUND, e)

    async def fetch_random_restaurants(self, code):
        try:
            restaurants = []
            cursor = self.collection_name.aggregate([
                {"$match": {"code": code, "is_available": True}},
                {"$sample": {"size": 5}}
            ])
            restaurants = await cursor.to_list(length=None)

            if len(restaurants) == 0:
                cursor = self.collection_name.aggregate([
                    {"$match": {"is_available": True}},
                    {"$sample": {"size": 5}}
                ])
                restaurants = await cursor.to_list(length=None)

            # is_found(restaurants)

            return list_serial(restaurants, individual_restaurant_serializer)

        except Exception as e:
            server_error(status.HTTP_404_NOT_FOUND, e)
