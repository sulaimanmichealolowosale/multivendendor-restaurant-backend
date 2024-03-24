from typing import List
from fastapi import APIRouter, status, HTTPException
from .restaurant_service import RestaurantService
from app.models.restaurant import Restaurant


router = APIRouter(
    prefix="/api/restaurant",
    tags=["Restaurant"]
)
restaurant_service = RestaurantService()


@router.get('/{code}')
async def fetch_all_restaurants(code: str):
    awaited_restaurants = await restaurant_service.fetch_all_restaurants(code)
    return awaited_restaurants


@router.post('/', status_code=status.HTTP_201_CREATED)
async def insert_restaurant(restaurant: Restaurant):
    new_restaurant = await restaurant_service.insert_restaurant(restaurant)
    return new_restaurant


@router.get('/by-id/{id}')
async def fetch_single_restaurant(id: str):
    single_restaurant = await restaurant_service.fetch_single_restaurant(id)
    return single_restaurant


@router.get('/random-restaurants/{code}')
async def fetch_random_restaurants(code: str):
    random_restaurant = await restaurant_service.fetch_random_restaurants(code)
    return random_restaurant


@router.get('/nearby-restaurants/{code}')
async def fetch_all_nearby_restaurants(code: str):
    random_restaurant = await restaurant_service.fetch_nearby_restaurants(code)
    return random_restaurant


@router.post('/insert_many')
async def insert_many_restaurants(restaurants: List[Restaurant]):
    many_restaurants = await restaurant_service.insert_many_restaurants(
        restaurants=restaurants)
    return many_restaurants
