from decouple import config

DATABASE_NAME = config('DATABASE_NAME', cast=str)
ENVIRONMENT = config('ENVIRONMENT', cast=str)
