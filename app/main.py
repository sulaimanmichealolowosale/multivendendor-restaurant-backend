from fastapi import FastAPI
from app.routes.category import category_controller
from app.routes.restaurant import restaurant_controller
from app.routes.food import food_controller
from app.routes.rating import rating_controller
from app.routes.auth import auth_controller
from app.routes.user import user_controller
from app.routes.address import address_controller
from app.routes.cart import cart_controller
from app.routes.order import order_controller
from fastapi.middleware.cors import CORSMiddleware


origin = ['*']

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origin,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


class Route:
    def __init__(self, *args) -> None:
        [app.include_router(keys.router) for keys in args]


app_route = Route(
    category_controller,
    restaurant_controller,
    food_controller,
    rating_controller,
    auth_controller,
    user_controller,
    address_controller,
    cart_controller,
    order_controller,
)


@app.get('/')
async def home():
    return {"messsage": "Welcome to the home page"}

# uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
