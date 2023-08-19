from fastapi import APIRouter, Depends, UploadFile
from fastapi.params import File
from starlette.staticfiles import StaticFiles

from src.auth.auth import get_current_user
from src.core.utils import process_uploaded_file
from src.models import user_pydantic

router = APIRouter(
    prefix='/media',
    tags=['Media']
)

router.mount('/static', StaticFiles(directory='src/static'), name='static')


@router.post('/uploadfile/profile')
async def create_upload_file_for_profile(
        file: UploadFile = File(...),
        user: user_pydantic = Depends(get_current_user)
) -> dict:
    return await process_uploaded_file(file, user)


@router.post('/uploadfile/product/{id}')
async def create_upload_file_for_product(
        id: int,
        file: UploadFile = File(...),
        user: user_pydantic = Depends(get_current_user)
) -> dict:
    return await process_uploaded_file(file, user, is_product=True)
