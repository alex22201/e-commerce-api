from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from src.auth.auth import get_current_user, token_generator
from src.auth.utils import get_hashed_password
from src.models import User, user_pydantic, user_pydantic_in

router = APIRouter(
    prefix='/auth',
    tags=['Auth']

)


@router.post('/token')
async def generate_token(
        request_form: OAuth2PasswordRequestForm = Depends()
) -> dict:
    print('ya tut')
    token = await token_generator(request_form.username, request_form.password)
    return {
        'access_token': token,
        'token_type': 'Bearer'
    }


@router.post('/user/me')
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
