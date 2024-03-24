from bson import ObjectId
from passlib.context import CryptContext
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType

from app.utils.get_env import settings


def validate_object_id(id):
    if not ObjectId.is_valid(id):
        raise ValueError(f"{id} is not a valid object id")


password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    hashed_password = password_context.hash(password)
    return hashed_password


def verify_password(plain_password, hashed_password):
    return password_context.verify(plain_password, hashed_password)


def define_email_html(login_email, password, username, otp):

    html = f"""
    <br>
    <h1>Welcome</h1>
    <h3>Here are your login details</h3>
    <p>Here are your details <br> Login_email:  {login_email} <br> Password: {password} <br> Username:{username}</P>
    <h4> Verification otp <h1>{otp}</h1> </h4>
    """

    return html


conf = ConnectionConfig(
    MAIL_USERNAME=str(settings.MAIL_USERNAME),
    MAIL_PASSWORD=str(settings.MAIL_PASSWORD),
    MAIL_FROM=str(settings.MAIL_FROM),
    MAIL_PORT=int(settings.MAIL_PORT),
    MAIL_SERVER=str(settings.MAIL_SERVER),
    MAIL_FROM_NAME=settings.MAIL_FROM_NAME,
    MAIL_SSL_TLS=True,
    MAIL_STARTTLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
)
