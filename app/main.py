from decouple import config
from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

app = FastAPI()


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
