from decouple import config

SECRET = config('SECRET', cast=str)
