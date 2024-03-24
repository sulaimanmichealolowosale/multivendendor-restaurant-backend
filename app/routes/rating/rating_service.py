from bson import ObjectId
from app.models.rating import Rating
from app.schemas.schema import individual_rating_serializer, list_serial
from app.utils.helper_functions import validate_object_id
from app.utils.messages import is_found, server_error
from app.config.database import motor_db
from fastapi import HTTPException, status


class RatingService:

    def __init__(self):
        self.collection_name = motor_db['rating']

    async def get_collection_name(self, collection_name: str):
        return motor_db[collection_name.lower()]

    async def insert_rating(self, rating: Rating):
        try:
            collection_name = await self.get_collection_name(rating.rating_type)
            product = await collection_name.find_one({"_id": ObjectId(rating.product_id)})
            if not product:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'''Unknown id : {
                                    rating.product_id} for {rating.rating_type}''')

            new_rating = await self.collection_name.insert_one(rating.model_dump())
            inserted_rating = await self.collection_name.find_one({"_id": new_rating.inserted_id})

            cursor = self.collection_name.aggregate([
                {
                    "$match": {
                        "rating_type": rating.rating_type,
                        "product_id": rating.product_id
                    }
                },
                {
                    "$group": {
                        "_id": "$product_id",
                        "average_rating": {"$avg": "$rating"}
                    }
                }
            ])
            ratings = await cursor.to_list(length=None)
            if len(ratings) > 0:
                average_rating = ratings[0]['average_rating']

                await collection_name.find_one_and_update(
                    {"_id": ObjectId(rating.product_id)},
                    {"$set": {"rating": average_rating}},
                    {"new": True}
                )

            return individual_rating_serializer(inserted_rating)
        except Exception as e:
            server_error(status.HTTP_500_INTERNAL_SERVER_ERROR, e)

    async def check_rating(self, user_id, product_id, rating_type):
        try:
            existing_rating = await self.collection_name.find_one({
                "user_id": user_id,
                "product_id": product_id,
                "rating_type": rating_type,
            })
            if existing_rating:
                return {"status": True, "message": f'''You have already rated this {rating_type}'''}
            else:
                return {"status": False, "message": f'''You are yet to rate this {rating_type}'''}

        except Exception as e:
            server_error(status.HTTP_404_NOT_FOUND, e)

    # async def fetch_ratings(self, rating):
    #     try:
    #         cursor:
    #     except Exception as e:
    #         server_error(status.HTTP_404_NOT_FOUND, e)
