from app.utils.get_env import settings
from motor.motor_asyncio import AsyncIOMotorClient


mongo_client = AsyncIOMotorClient(f'''mongodb+srv://{settings.mongodb_username}:{
                                  settings.mongodb_password}@mikecluster.s92yre1.mongodb.net/?retryWrites=true&w=majority''')
# mongo_client = AsyncIOMotorClient("mongodb://localhost:27017")
motor_db = mongo_client[f'{settings.mongodb}']
