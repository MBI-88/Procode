from .base_setting import *

# Develop config
DEBUG = config('DEBUG',cast=bool,default=True)
SECRET_KEY = config('SECRET_KEY')
EMAIL_BACKEND = config('EMAIL_BACKEND')
EMAIL_HOST = config('EMAIL_HOST') # Put your e-mail admin
EMAIL_PORT = config('EMAIL_PORT',cast=int) # Put your port 
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = config('EMAIL_USE_TLS',default=True,cast=bool)
EMAIL_USE_SSL = config('EMAIL_USE_SSL',default=True,cast=bool)

DATABASES = {
    'default': {
        'ENGINE': config('DB_ENGINE'),
        'NAME': BASE_DIR / config('DB_NAME'),
    }
}

MEDIA_URL = config('MEDIA_URL')
MEDIA_ROOT = os.path.join(BASE_DIR,config('MEDIA_ROOT')) 
