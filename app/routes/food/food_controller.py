from typing import List
from fastapi import APIRouter, status
from app.models.food import Food
from .food_service import FoodService


router = APIRouter(
    prefix="/api/foods",
    tags=["Food"]
)
food_service = FoodService()


@router.get('/')
async def fetch_all_foods():
    awaited_foods = await food_service.fetch_all_foods()
    return awaited_foods


@router.post('/', status_code=status.HTTP_201_CREATED)
async def insert_food(food: Food):
    new_food = await food_service.insert_food(food)
    return new_food


@router.get('/{id}')
async def fetch_single_food(id: str):
    single_food = await food_service.fetch_single_food(id)
    return single_food


@router.get('/nearby-foods/{code}')
async def fetch_nearby_foods(code: str):
    random_restaurant = await food_service.fetch_nearby_foods(code)
    return random_restaurant


@router.get('/recommendations/{code}')
async def recommendations_by_code(code: str):
    random_food = await food_service.recommendations_by_code(code)
    return random_food


@router.get('/restaurant-foods/{id}')
async def fetch_foods_by_restaurant(id: str):
    random_food = await food_service.fetch_foods_by_restaurant(id)
    return random_food


@router.get('/{code}/{category}')
async def get_foods_by_category_and_code(code: str, category: str):
    random_restaurant = await food_service.get_foods_by_category_and_code(code, category)
    return random_restaurant


@router.get('/random/{code}/{category}')
async def get_random_foods_by_category_and_code(code: str, category: str):
    random_restaurant = await food_service.get_random_foods_by_category_and_code(code, category)
    return random_restaurant


@router.get('/search/foods/{search_term}')
async def search_food(search_term: str):
    random_restaurant = await food_service.search_food(search_term)
    return random_restaurant


@router.post('/insert_many')
async def insert_many_foods(foods: List[Food]):
    many_foods = await food_service.insert_many_foods(
        foods=foods)
    return many_foods
