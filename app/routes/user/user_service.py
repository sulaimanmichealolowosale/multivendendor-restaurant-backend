from bson import ObjectId
from app.schemas.schema import individual_user_serializer, list_serial
from app.utils.messages import is_found, server_error
from app.config.database import motor_db
from fastapi import HTTPException, status


class UserService:

    def __init__(self):
        self.collection_name = motor_db['user']

    async def get_user(self, id: str):
        try:
            user = await self.collection_name.find_one({"_id": ObjectId(id)})
            return individual_user_serializer(user)

        except Exception as e:
            server_error(status_code=status.HTTP_404_NOT_FOUND, e=e)

    async def get_users(self):
        try:
            cursor = self.collection_name.find({"verification": True})

            users = await cursor.to_list(length=None)
            is_found(users)
            return list_serial(users, individual_user_serializer)
        except Exception as e:
            server_error(status_code=status.HTTP_404_NOT_FOUND, e=e)

    async def verify_account(self, id: str, otp):
        try:
            user = await self.collection_name.find_one({"_id": ObjectId(id)})

            if user is not None:
                if otp == user['otp']:
                    user['verification'] = True
                    await self.collection_name.find_one_and_update(
                        {"_id": ObjectId(id)},
                        {"$set": {"verification": True, "otp": "none"}}
                    )
                    return individual_user_serializer(user)
                else:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND, detail="Otp verification failed")
        except Exception as e:
            server_error(status_code=status.HTTP_404_NOT_FOUND, e=e)

    async def verify_phone(self, id: str, phone):
        try:
            user = await self.collection_name.find_one({"_id": ObjectId(id)})

            if user is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
            await self.collection_name.find_one_and_update(
                {"_id": ObjectId(id)},
                {"$set": {"phone_verification": True, "phone": phone}}
            )
            user['phone'] = phone
            user['phone_verification'] = True
            return individual_user_serializer(user)

        except Exception as e:
            server_error(status_code=status.HTTP_404_NOT_FOUND, e=e)
