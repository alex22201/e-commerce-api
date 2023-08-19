from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, UploadFile, status
from fastapi.params import File

from src.auth.auth import get_current_user
from src.core.utils import process_uploaded_file
from src.models import (Business, Product, business_pydantic,
                        business_pydantic_in, product_pydantic,
                        product_pydantic_in, user_pydantic)

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


@router_core.post('/products')
async def add_new_product(
        product: product_pydantic_in,
        user: user_pydantic = Depends(get_current_user)
) -> dict:
    product = product.dict(exclude_unset=True)
    if product['original_price'] > 0:
        product['discount_percent'] = ((product['original_price'] - product['new_price']) / product[
            'original_price']) * 100
        print(product)
        print(user)
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
        await product.delete()
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Not authorized to perform this action',
            headers={'WWW-Authenticate': 'Bearer'}
        )
    return {
        'status': 'ok'
    }


@router_core.put('/product/{product_id}')
async def update_product(
        product_id: int,
        update_info: product_pydantic_in,
        user: user_pydantic = Depends(get_current_user)
) -> dict:
    product = await Product.get(id=product_id)
    business = await product.business
    owner = await business.owner

    update_info = update_info.dict(exclude_unset=True)
    update_info['date_published'] = datetime.utcnow()

    if user == owner and update_info['original_price'] != 0:
        update_info['discount_percent'] = ((update_info['original_price'] - update_info['new_price']) / update_info[
            'original_price']) * 100
        product = await product.update_from_dict(update_info)
        await product.save()

        response = await product_pydantic.from_tortoise_orm(product)
        return {
            'status': 'ok',
            'data': response
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Not authorized to perform this action or invalid user input',
            headers={'WWW-Authenticate': 'Bearer'}
        )


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
                'business_id': business.id,
                'join_date': owner.join_date.strftime('%b %d %Y')
            }
        }
    }


@router_core.get('/products/get')
async def get_products() -> dict:
    response = await product_pydantic.from_queryset(Product.all())
    return {
        'status': 'ok',
        'data': response
    }


@router_core.put('/business/{business_id}')
async def update_business(
        business_id: int,
        update_info: business_pydantic_in,
        user: user_pydantic = Depends(get_current_user)
) -> dict:
    update_info = update_info.dict()
    business = await Business.get(id=business_id)
    business_owner = await business.owner

    update_info['date_published'] = datetime.utcnow()

    if user == business_owner:
        product = await business.update_from_dict(update_info)
        await product.save()

        response = await business_pydantic.from_tortoise_orm(business)
        return {
            'status': 'ok',
            'data': response
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Not authorized to perform this action',
            headers={'WWW-Authenticate': 'Bearer'}
        )
