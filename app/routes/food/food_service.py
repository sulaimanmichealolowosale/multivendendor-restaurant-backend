from typing import List
from bson import ObjectId
from app.models.food import Food
from app.schemas.schema import individual_food_serializer, list_serial
from app.utils.helper_functions import validate_object_id
from app.utils.messages import is_found, server_error
from app.config.database import motor_db
from fastapi import status


class FoodService:

    def __init__(self):
        self.collection_name = motor_db['food']

    async def insert_many_foods(self, foods: List[Food]):
        try:
            await self.collection_name.insert_many([food.model_dump() for food in foods])
            return {"Message": "Foods Inserted successfully"}
        except Exception as e:
            print(e)

    async def insert_food(self, food: Food):
        try:
            new_food = await self.collection_name.insert_one(food.model_dump())
            inserted_food = await self.collection_name.find_one({"_id": new_food.inserted_id})
            return individual_food_serializer(inserted_food)

        except Exception as e:
            server_error(status.HTTP_500_INTERNAL_SERVER_ERROR, e)

    async def fetch_all_foods(self):
        try:
            cursor = self.collection_name.find()
            foods = await cursor.to_list(length=None)
            # is_found(foods)
            return list_serial(foods, individual_food_serializer)
        except Exception as e:
            server_error(status.HTTP_404_NOT_FOUND, e)

    async def fetch_single_food(self, food_id):
        try:
            food = await self.collection_name.find_one(
                {"_id": ObjectId(food_id)}
            )
            return individual_food_serializer(food)
        except Exception as e:
            server_error(status.HTTP_404_NOT_FOUND, e)

    async def fetch_nearby_foods(self, code):
        try:
            foods = []
            cursor = self.collection_name.aggregate([
                {"$match": {"code": code, "is_available": True}},
            ])
            foods = await cursor.to_list(length=None)

            if len(foods) == 0:
                cursor = self.collection_name.aggregate([
                    {"$match": {"is_available": True}},
                ])
                foods = await cursor.to_list(length=None)
            # is_found(foods)
            return list_serial(foods, individual_food_serializer)

        except Exception as e:
            server_error(status.HTTP_404_NOT_FOUND, e)

    async def recommendations_by_code(self, code):
        try:
            cursor = self.collection_name.aggregate([
                {"$match": {"code": code, "is_available": True}},
                {"$sample": {"size": 5}}
            ])
            foods = await cursor.to_list(length=None)

            if len(foods) == 0:
                cursor = self.collection_name.aggregate([
                    {"$match": {"is_available": True}},
                    {"$sample": {"size": 5}}
                ])
                foods = await cursor.to_list(length=None)
            # is_found(foods)
            return list_serial(foods, individual_food_serializer)

        except Exception as e:
            server_error(status.HTTP_404_NOT_FOUND, e)

    async def fetch_foods_by_restaurant(self, id):
        try:
            validate_object_id(id)
            cursor = self.collection_name.find(
                {"restaurant": id, "is_available": True})
            foods = await cursor.to_list(length=None)
            # is_found(foods)
            return list_serial(foods, individual_food_serializer)
        except Exception as e:
            server_error(status.HTTP_404_NOT_FOUND, e)

    async def get_foods_by_category_and_code(self,  code, category):
        try:
            cursor = self.collection_name.aggregate([
                {"$match": {"category": category, "code": code, "is_available": True}}
            ])
            foods = await cursor.to_list(length=None)
            # if foods == None:
            #     cursor = self.collection_name.aggregate([
            #         {"$match": {"category": category, "is_available": True}}
            #     ])
            #     foods = await cursor.to_list(length=None)
            # is_found(foods)
            return list_serial(foods, individual_food_serializer)
        except Exception as e:
            server_error(status.HTTP_404_NOT_FOUND, e)

    async def get_random_foods_by_category_and_code(self,  code, category):
        try:
            cursor = self.collection_name.aggregate([
                {"$match": {"category": category, "code": code, "is_available": True}},
                {"$sample": {"size": 10}}
            ])
            foods = await cursor.to_list(length=None)

            if len(foods) == 0:
                cursor = self.collection_name.aggregate([
                    {"$match": {"code": code, "is_available": True}},
                    {"$sample": {"size": 10}}
                ])
                foods = await cursor.to_list(length=None)
                if len(foods) == 0:
                    cursor = self.collection_name.aggregate([
                        {"$match": {"is_available": True}},
                        {"$sample": {"size": 10}}
                    ])
                    foods = await cursor.to_list(length=None)
            # is_found(foods)
            return list_serial(foods, individual_food_serializer)
        except Exception as e:
            server_error(status.HTTP_404_NOT_FOUND, e)

    async def search_food(self, search_term: str):
        try:
            cursor = self.collection_name.aggregate([
                {"$search": {
                    "index": "foods",
                    "text": {
                        "query": f"{search_term}",
                        "path": {"wildcard": "*"}
                    }
                }
                }
            ])
            foods = await cursor.to_list(length=None)
            # is_found(foods)
            return list_serial(foods, individual_food_serializer)
        except Exception as e:
            server_error(status.HTTP_404_NOT_FOUND, e)
