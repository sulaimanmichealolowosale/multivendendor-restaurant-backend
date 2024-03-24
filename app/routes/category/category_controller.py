from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from app.utils.oauth2 import get_current_admin, get_current_user

from .category_service import CategoryService
from app.models.category import Category


router = APIRouter(
    prefix="/api/category",
    tags=["Category"]
)
categorie_service = CategoryService()


@router.get('/')
async def fetch_all_categories():
    awaited_categories = await categorie_service.fetch_all_categories()
    return awaited_categories


@router.post('/', status_code=status.HTTP_201_CREATED)
async def insert_category(category: Category):
    new_category = await categorie_service.insert_category(category)
    return new_category


@router.post('/insert-many', status_code=status.HTTP_201_CREATED)
async def insert_many_category(categories: List[Category]):
    new_category = await categorie_service.insert_many_categories(categories)
    return new_category


@router.get('/random-categories')
async def fetch_random_categories():
    random_categories = await categorie_service.fetch_random_categories()
    return random_categories
