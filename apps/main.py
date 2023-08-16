from typing import List, Optional, Type

import jwt
from decouple import config
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from tortoise import BaseDBAsyncClient
from tortoise.contrib.fastapi import register_tortoise
from tortoise.signals import post_save

from auth import get_hashed_password, token_generator
from models import (Business, User, business_pydantic, user_pydantic,
                    user_pydantic_in)

app = FastAPI()

oath2_scheme = OAuth2PasswordBearer(tokenUrl='token')


@app.post('/token')
async def generate_token(
        request_form: OAuth2PasswordRequestForm = Depends()
) -> dict:
    token = await token_generator(request_form.username, request_form.password)
    return {
        'access_token': token,
        'token_type': 'Bearer'
    }


async def get_current_user(
        token: str = Depends(oath2_scheme)
) -> User:
    try:
        payload = jwt.decode(
            token,
            config('SECRET', cast=str),
            algorithms=['HS256'])

        user = await User.get(id=payload.get('id'))

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid username or password',
            headers={'WWW-Authenticate': 'Bearer'}
        )
    return await user


@app.post('/user/me')
async def user_login(
        user: user_pydantic_in = Depends(get_current_user)
) -> dict:
    # business = await Business.get(owner=user)
    return {
        'status': 'ok',
        'username': user.username,
        'email': user.email,
        'verified': user.is_verified,
        'join_date': user.join_date.strftime('%b %d %Y')
    }


@post_save(User)
async def create_business(
        sender: 'Type[User]',
        instance: User,
        created: bool,
        using_db: 'Optional[BaseDBAsyncClient]',
        update_fields: List[str]
) -> None:
    if created:
        business_obj: Business = await Business.create(
            name=instance.username,
            owner=instance
        )
        await business_pydantic.from_tortoise_orm(business_obj)


@app.post('/registration')
async def user_registration(user: user_pydantic_in) -> dict:
    user_info = user.dict(exclude_unset=True)
    user_info['password'] = get_hashed_password(user_info['password'])
    user_obj = await User.create(**user_info)
    new_user: User = await user_pydantic.from_tortoise_orm(user_obj)

    return {
        'status': 'ok',
        'data': f'Hello {new_user.username}, thanks for join us!'
    }


@app.get('/')
def index():
    return {'Message': 'Hello world'}


DATABASE = config('DB_URL', cast=str)

register_tortoise(
    app,
    db_url=DATABASE,
    modules={'models': ['models']},
    generate_schemas=True,
    add_exception_handlers=True
)
