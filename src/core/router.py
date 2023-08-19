from fastapi import APIRouter, Depends, HTTPException, UploadFile, status
from fastapi.params import File

from src.auth.auth import get_current_user
from src.core.utils import process_uploaded_file
from src.models import Product, product_pydantic, user_pydantic

router_media = APIRouter(
    prefix='/media',
    tags=['Media']
)


@router_media.post('/uploadfile/profile')
async def create_upload_file_for_profile(
        file: UploadFile = File(...),
        user: user_pydantic = Depends(get_current_user)
) -> dict:
    return await process_uploaded_file(file, user)


@router_media.post('/uploadfile/product/{id}')
async def create_upload_file_for_product(
        product_id: int,
        file: UploadFile = File(...),
        user: user_pydantic = Depends(get_current_user)
) -> dict:
    return await process_uploaded_file(file, user,
                                       is_product=True,
                                       product_id=product_id
                                       )


router_core = APIRouter(
    prefix='/core',
    tags=['Core']
)


@router_core.post('/product/add')
async def add_new_product(
        product: product_pydantic,
        user: user_pydantic = Depends(get_current_user)
) -> dict:
    product = product.dict(exclude_unset=True)
    if product['original_price'] > 0:
        product['discount_percent'] = ((product['original_price'] - product['new_price']) / product[
            'original_price']) * 100

        product_obj = await Product.create(**product, business=user)
        product_obj = await product_pydantic.from_tortoise_orm(
            product_obj
        )
        return {
            'status': 'ok',
            'data': product_obj
        }
    return {
        'status': 'error'
    }


@router_core.delete('/product/remove/{product_id}')
async def delete_product(
        product_id: int,
        user: user_pydantic = Depends(get_current_user)
) -> dict:
    product = await Product.get(id=product_id)
    business = await product.business
    owner = await business.owner

    if user == owner:
        product.delete()
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Not authorized to perform this action',
            headers={'WWW-Authenticate': 'Bearer'}
        )
    return {
        'status': 'ok'
    }


@router_core.get('/product/get/{product_id}')
async def get_product_by_id(product_id: int) -> dict:
    product = await Product.get(id=product_id)
    business = await product.business
    owner = await business.owner
    response = await product_pydantic.from_queryset_single(Product.get(id=product_id))

    return {
        'status': 'ok',
        'data': {
            'product_details': response,
            'business_details': {
                'name': business.name,
                'city': business.city,
                'region': business.region,
                'description': business.description,
                'logo': business.logo,
                'owner_id': owner.id,
                'join_date': owner.join_date.strftime('%b %d %Y')
            }
        }
    }


@router_core.get('/product')
async def get_products() -> dict:
    response = await product_pydantic.from_queryset(Product.all())
    print(response)
    return {
        'status': 'ok',
        'data': response
    }
