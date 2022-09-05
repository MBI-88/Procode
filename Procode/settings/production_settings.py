from base_setting import *

# Production config

DEBUG = config('DEBUG',cast=bool,default=False)
SECRET_KEY =  config('SECRET_KEY')
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
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT',cast=int),
        'PASSWORD': config('DB_PASSWORD'),
    }
}

