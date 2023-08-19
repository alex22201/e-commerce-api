from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from src.auth.router import router as router_auth
from src.config import DATABASE, ENVIRONMENT
from src.core.router import router as router_core

app = FastAPI(
    title='Study project',
    debug=True if ENVIRONMENT == ['local', 'test'] else False
)

app.include_router(
    router_auth
)

app.include_router(
    router_core
)


@app.get('/', tags=["Welcome"])
def index():
    return {'Message': 'Welcome to my project!'}


register_tortoise(
    app,
    db_url=DATABASE,
    modules={'models': ['src.models']},
    generate_schemas=True,
    add_exception_handlers=True
)
