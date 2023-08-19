from decouple import config

FILEPATH = config('FILEPATH', cast=str)

allowed_extensions = ['png', 'jpg']
