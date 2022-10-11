from .base_setting import *

# Develop config
DEBUG = config('DEBUG',cast=bool,default=True)
SECRET_KEY = config('SECRET_KEY')
EMAIL_BACKEND = config('EMAIL_BACKEND')
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_PORT = config('EMAIL_PORT',cast=int)

DATABASES = {
    'default': {
        'ENGINE': config('DB_ENGINE'),
        'NAME': BASE_DIR / config('DB_NAME'),
    }
}

MEDIA_URL = config('MEDIA_URL')
MEDIA_ROOT = os.path.join(BASE_DIR,config('MEDIA_ROOT')) 
