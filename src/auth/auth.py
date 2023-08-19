import jwt
from fastapi import Depends, HTTPException, status

from src.auth.config import SECRET
from src.auth.constants import oath2_scheme
from src.auth.utils import verify_password
from src.models import User


async def get_current_user(
        token: str = Depends(oath2_scheme)
) -> User:
    try:
        payload = jwt.decode(
            token,
            SECRET,
            algorithms=['HS256'])

        user = await User.get(id=payload.get('id'))

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid username or password',
            headers={'WWW-Authenticate': 'Bearer'}

        )
    return await user


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
    token = jwt.encode(token_data, SECRET)

    return token
