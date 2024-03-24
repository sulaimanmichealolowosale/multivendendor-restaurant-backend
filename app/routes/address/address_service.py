from bson import ObjectId
from app.models.address import Address
from app.schemas.schema import individual_address_serializer, list_serial
from app.utils.messages import is_found, server_error
from app.config.database import motor_db
from fastapi import HTTPException, status


class AddressService:

    def __init__(self):
        self.collection_name = motor_db['address']
        self.user_collection_name = motor_db['user']

    async def get_collection_name(self, collection_name: str):
        return motor_db[collection_name.lower()]

    async def add_address(self, address: Address):
        try:
            if address.default == True:
                await self.collection_name.update_many(
                    {"user_id": address.user_id},
                    {"$set": {"default": False}}
                )

            new_address = await self.collection_name.insert_one(address.model_dump())
            inserted_address = await self.collection_name.find_one({"_id": ObjectId(new_address.inserted_id)})
            return individual_address_serializer(inserted_address)
        except Exception as e:
            server_error(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, e=e)

    async def get_addresses(self, user_id: str):
        try:
            cursor = self.collection_name.find({"user_id": user_id})
            addresses = await cursor.to_list(length=None)
            is_found(addresses)
            return list_serial(addresses, individual_address_serializer)
        except Exception as e:
            server_error(status_code=status.HTTP_404_NOT_FOUND, e=e)

    async def set_default_address(self, user_id: str, address_id: str):
        try:

            user = await self.user_collection_name.find_one(
                {"_id": ObjectId(user_id)})
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

            await self.collection_name.update_many(
                {"user_id": user_id},
                {"$set": {"default": False}}
            )
            address = await self.collection_name.find_one_and_update(
                {"_id": ObjectId(address_id)},
                {"$set": {"default": True}})

            if address:
                await self.user_collection_name.find_one_and_update(
                    {"_id": ObjectId(user_id)},
                    {"$set": {"address": address_id}}
                )

            address['default'] = True

            return individual_address_serializer(address)
        except Exception as e:
            server_error(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, e=e)

    async def get_default_address(self, user_id):
        try:
            user = await self.user_collection_name.find_one(
                {"_id": ObjectId(user_id)})
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

            address = await self.collection_name.find_one({"user_id": user_id, "default": True})
            return individual_address_serializer(address)
        except Exception as e:
            server_error(
                status_code=status.HTTP_404_NOT_FOUND, e=e)
