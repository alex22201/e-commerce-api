from typing import List

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from tortoise.signals import post_save

from src.auth.auth import get_current_user, token_generator
from src.auth.utils import get_hashed_password
from src.models import (Business, User, business_pydantic, user_pydantic,
                        user_pydantic_in)

router = APIRouter(
    prefix='/auth',
    tags=['Auth']

)


@router.post('/token')
async def generate_token(
        request_form: OAuth2PasswordRequestForm = Depends()
) -> dict:
    token = await token_generator(request_form.username, request_form.password)
    return {
        'access_token': token,
        'token_type': 'Bearer'
    }


@router.post('/user/me')
async def user_login(
        user: user_pydantic_in = Depends(get_current_user)
) -> dict:
    business = await Business.get(owner=user)
    logo = business.logo
    logo_path = f'localhost:8000/static/images/{logo}'
    return {
        'status': 'ok',
        'data': {
            'username': user.username,
            'email': user.email,
            'verified': user.is_verified,
            'join_date': user.join_date.strftime('%b %d %Y'),
            'logo': logo_path
        }
    }


@router.post('/registration')
async def user_registration(user: user_pydantic_in) -> dict:
    user_info = user.dict(exclude_unset=True)
    user_info['password'] = get_hashed_password(user_info['password'])
    user_obj = await User.create(**user_info)
    new_user: User = await user_pydantic.from_tortoise_orm(user_obj)

    return {
        'status': 'ok',
        'data': f'Hello {new_user.username}, thanks for join us!'
    }


# signals
@post_save(User)
async def create_business(
        sender: 'Type[User]',  # noqa
        instance: User,
        created: bool,
        using_db: 'Optional[BaseDBAsyncClient]',  # noqa
        update_fields: List[str]  # noqa
) -> None:
    if created:
        business_obj: Business = await Business.create(
            name=instance.username,
            owner=instance
        )
        await business_pydantic.from_tortoise_orm(business_obj)
