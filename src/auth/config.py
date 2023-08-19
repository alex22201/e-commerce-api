from decouple import config

SECRET = config('SECRET', cast=str)
FILEPATH = config('FILEPATH', cast=str)
