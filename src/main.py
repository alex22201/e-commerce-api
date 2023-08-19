from fastapi import FastAPI
from starlette.staticfiles import StaticFiles
from tortoise.contrib.fastapi import register_tortoise

from src.auth.router import router as router_auth
from src.config import DATABASE_NAME, ENVIRONMENT
from src.core.router import router_core, router_media

app = FastAPI(
    title='Study project',
    debug=True if ENVIRONMENT == ['local', 'test'] else False
)
app.mount('/static', StaticFiles(directory='static'), name='static')

app.include_router(
    router_auth
)

app.include_router(
    router_media
)

app.include_router(
    router_core
)


@app.get('/', tags=["Welcome"])
def index():
    return {'Message': 'Welcome to my project!'}


register_tortoise(
    app,
    db_url=f'sqlite://./{DATABASE_NAME}',
    modules={'models': ['src.models']},
    generate_schemas=True,
    add_exception_handlers=True
)
