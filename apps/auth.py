import jwt
from decouple import config
from fastapi import HTTPException, status
from models import User
from passlib.context import CryptContext

password_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def get_hashed_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_context.verify(plain_password, hashed_password)


async def authenticate_user(username: str, password: str):
    user = await User.get(username=username)

    if user and verify_password(password, user.password):
        return user
    return False


async def token_generator(username: str, password: str) -> str:
    user = await authenticate_user(username, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid username or password',
            headers={'WWW-Authenticate': 'Bearer'}

        )
    token_data = {
        'id': user.id,
        'username': user.username
    }
    token = jwt.encode(token_data, config('SECRET', cast=str))

    return token
