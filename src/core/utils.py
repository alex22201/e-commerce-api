import secrets
import socket

from fastapi import HTTPException, UploadFile, status
from PIL import Image

from src.core.config import FILEPATH, allowed_extensions
from src.models import Business, Product


def check_file_extension(extension: str):
    if extension not in allowed_extensions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='File extension not allowed'
        )


async def process_uploaded_file(file: UploadFile, user, is_product=False, id=None):
    filename = file.filename
    extension = filename.split('.')[-1].lower()
    check_file_extension(extension)

    token_name = secrets.token_hex(10) + '.' + extension
    generated_name = FILEPATH + token_name
    file_content = await file.read()

    with open(generated_name, 'wb') as f:
        f.write(file_content)

    img = Image.open(generated_name)
    img = img.resize(size=(200, 200))
    img.save(generated_name)

    f.close()

    if is_product:
        item = await Product.get(id=id)
        related_item = await item.business
    else:
        item = await Business.get(owner=user)
        related_item = item

    owner = await related_item.owner

    if owner != user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Not authorized to perform this action',
            headers={'WWW-Authenticate': 'Bearer'}
        )

    if is_product:
        item.product_image = token_name
    else:
        item.logo = token_name

    await item.save()

    hostname = socket.gethostname()
    file_url = hostname + generated_name[1:]
    return {
        'status': 'ok',
        'filename': file_url
    }
