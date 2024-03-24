from typing import List
from app.models.category import Category
from app.schemas.schema import list_serial, individual_category_serializer
from app.config.database import motor_db
from app.utils.messages import server_error
from fastapi import HTTPException, status


class CategoryService:

    def __init__(self):
        self.collection_name = motor_db['category']

    async def insert_many_categories(self, categories: List[Category]):
        try:
            await self.collection_name.insert_many([categorie.model_dump() for categorie in categories])
            return {"Message": "Categories Inserted successfully"}
        except Exception as e:
            print(e)

    async def insert_category(self, category: Category):
        try:
            existing_category = await self.collection_name.find_one({"title": category.title})
            if existing_category:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"A category with title {
                                    category.title} already exists")
            new_category = await self.collection_name.insert_one(category.model_dump())
            inserted_category = await self.collection_name.find_one({"_id": new_category.inserted_id})
            return individual_category_serializer(inserted_category)

        except Exception as e:
            server_error(status.HTTP_500_INTERNAL_SERVER_ERROR, e)

    async def fetch_all_categories(self):
        try:
            cursor = self.collection_name.find(
                {"title": {"$ne": "More"}},
                {"_v": 0}
            )
            categories = await cursor.to_list(length=None)
            return list_serial(categories, individual_category_serializer)
        except Exception as e:
            server_error(status.HTTP_404_NOT_FOUND, e)

    async def fetch_random_categories(self):
        try:
            cursor = self.collection_name.aggregate([
                {"$match": {"title": {"$ne": "More"}}},
                {"$sample": {"size": 4}}
            ])

            random_categories = await cursor.to_list(length=None)

            more_category = await self.collection_name.find_one(
                {"title": "More"}, {"_v": 0})

            if more_category is not None:
                random_categories.append(more_category)

            return list_serial(random_categories, individual_category_serializer)

        except Exception as e:
            server_error(status.HTTP_404_NOT_FOUND, e)
