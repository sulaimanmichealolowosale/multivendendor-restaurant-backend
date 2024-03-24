from bson import ObjectId
from fastapi.security import OAuth2PasswordBearer
from datetime import timedelta, datetime
from fastapi import Depends, HTTPException, status
from app.models.auth import TokenData
from app.config.database import motor_db
from app.utils.get_env import settings
from jose import jwt
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")

SECRET_KEY = str(settings.SECRET_KEY)
ALGORITHM = str(settings.ALGORITHM)
ACCESS_TOKEN_EXPIRE_MINUTES = str(settings.ACCESS_TOKEN_EXPIRE_MINUTES)


def create_access_token(data: dict, expire_time: timedelta = None):  # type: ignore

    to_encode = data.copy()
    if expire_time:
        expire = datetime.utcnow()+expire_time
    else:
        time = int(ACCESS_TOKEN_EXPIRE_MINUTES)
        expire = datetime.utcnow() + timedelta(minutes=time)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id = payload.get('id')

        if id is None:
            raise credentials_exception

        token_data = TokenData(id=id)

    except Exception:
        raise credentials_exception

    return token_data


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN, detail="Could not validate credentials")
    auth = verify_access_token(
        token=token, credentials_exception=credentials_exception)
    collection_name = motor_db['user']

    user = await collection_name.find_one({"_id": ObjectId(auth.id)})
    return user


async def get_current_admin(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN, detail="You are unauthorized")
    auth = verify_access_token(
        token=token, credentials_exception=credentials_exception)
    collection_name = motor_db['user']

    user = await collection_name.find_one({"_id": ObjectId(auth.id)})

    if user is not None and user['user_type'] != "Admin":
        raise credentials_exception

    return user


async def get_current_driver(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN, detail="You are unauthorized")
    auth = verify_access_token(
        token=token, credentials_exception=credentials_exception)
    collection_name = motor_db['user']

    user = await collection_name.find_one({"_id": ObjectId(auth.id)})

    if user is not None and user['user_type'] != "Driver":
        raise credentials_exception

    return user


async def get_current_vendor(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN, detail="You are unauthorized")
    auth = verify_access_token(
        token=token, credentials_exception=credentials_exception)
    collection_name = motor_db['user']

    user = await collection_name.find_one({"_id": ObjectId(auth.id)})

    if user is not None and user['user_type'] != "Vendor":
        raise credentials_exception

    return user


async def get_current_client(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN, detail="You are unauthorized")
    auth = verify_access_token(
        token=token, credentials_exception=credentials_exception)
    collection_name = motor_db['user']

    user = await collection_name.find_one({"_id": ObjectId(auth.id)})

    if user is not None and user['user_type'] != "Client":
        raise credentials_exception

    return user
