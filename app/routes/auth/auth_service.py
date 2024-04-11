from datetime import timedelta
from bson import ObjectId
from fastapi_mail import FastMail, MessageSchema
from app.models.auth import Login
from app.models.user import User
from app.schemas.schema import individual_user_serializer
from app.utils.helper_functions import hash_password, define_email_html, conf, verify_password
from app.utils.messages import server_error
from app.config.database import motor_db
from fastapi import HTTPException, status
from app.utils.oauth2 import create_access_token
from fastapi import Response
from fastapi.security import OAuth2PasswordRequestForm

from app.utils.otp_generator import generate_otp


class AuthService:

    def __init__(self):
        self.collection_name = motor_db['user']

    async def send_otp_to_email(
        self,
        subject: str,
        email_to: str,
        login_email: str,
        password: str,
        username: str,
        otp: str
    ):
        message = MessageSchema(
            subject=subject,
            recipients=[email_to],
            subtype='html',  # type: ignore
            body=define_email_html(
                login_email=login_email, password=password, username=username, otp=otp),
        )

        fast_mail = FastMail(conf)

        await fast_mail.send_message(message)

    async def register(self, user: User):
        try:
            existing_email = await self.collection_name.find_one(
                {"email": user.email})
            if existing_email:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")

            otp = generate_otp()
            password = user.password
            hashed_password = hash_password(user.password)
            user.password = hashed_password
            user.otp = otp
            await self.send_otp_to_email(
                subject="Multivendor Restaurants",
                email_to=user.email,
                login_email=user.email,
                username=user.username,
                password=password,
                otp=otp
            )

            new_user = await self.collection_name.insert_one(user.model_dump())
            inserted_user = await self.collection_name.find_one({"_id": new_user.inserted_id})
            return individual_user_serializer(inserted_user, "")

        except Exception as e:
            server_error(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, e=e)

    async def login(self, login_details: Login, response: Response):
        try:
            user = await self.collection_name.find_one(
                {"email": login_details.email})
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Account no found")

            if not verify_password(plain_password=login_details.password, hashed_password=user['password']):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

            access_token = create_access_token(
                data={
                    "id": str(user['_id']),
                    "user_type": user['user_type'],
                    "verification": user['verification'],
                }
            )

            refresh_token = create_access_token(
                data={
                    "id": str(user['_id']),
                    "user_type": user['user_type'],
                    "verification": user['verification'],
                },
                expire_time=timedelta(days=1))
            response.set_cookie("refresh_token", refresh_token, httponly=True)
            response.set_cookie("access_token", access_token, httponly=True)
            # print(login_details)
            return individual_user_serializer(user, access_token)

        except Exception as e:
            server_error(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, e=e)

    async def logout(self, response: Response):
        try:
            response.delete_cookie("refresh_token")
            response.delete_cookie("access_token")

            return {
                "message": "Successfully logged out",

            }

        except Exception as e:
            print(e)
