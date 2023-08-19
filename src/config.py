from decouple import config

DATABASE = config('DB_URL', cast=str)
ENVIRONMENT = config('ENVIRONMENT', cast=str)
