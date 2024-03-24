from fastapi import APIRouter, status
from app.models.food import Food
from app.models.rating import Rating
from .rating_service import RatingService

router = APIRouter(
    prefix="/api/rating",
    tags=["Rating"]
)
rating_service = RatingService()


@router.post('/')
async def insert_rating(rating: Rating):

    new_rating = await rating_service.insert_rating(rating)
    return new_rating


@router.get('/{user_id}/{product_id}/{rating_type}')
async def check_rating(user_id: str, product_id: str, rating_type: str):
    check_rating = await rating_service.check_rating(user_id=user_id, product_id=product_id, rating_type=rating_type)
    return check_rating
