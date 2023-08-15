from typing import List, Optional, Type

from auth import get_hashed_password
from decouple import config
from fastapi import FastAPI
from models import (Business, User, business_pydantic, user_pydantic,
                    user_pydantic_in)
from tortoise import BaseDBAsyncClient
from tortoise.contrib.fastapi import register_tortoise
from tortoise.signals import post_save

app = FastAPI()


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
        # TODO
        # send the email


@app.post('/registration')
async def user_registration(user: user_pydantic_in) -> dict:
    user_info = user.dict(exclude_unset=True)
    user_info['password'] = get_hashed_password(user_info['password'])
    user_obj = await User.create(**user_info)
    new_user: User = await user_pydantic.from_tortoise_orm(user_obj)

    return {
        'status': 'ok',
        'data': f'Hello {new_user.username}, thanks for join us! Please '
                f'check your email to confirm your registration.'
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
