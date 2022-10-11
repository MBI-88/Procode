from .base_setting import *

# Develop config
DEBUG = True
SECRET_KEY = 'django-Secure-tx^m9&!dk1pdfri*+R03+28-&#^^x-cph^aknzv60l9x&dwxbkc'
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST='localhost'
EMAIL_PORT='1025'
EMAIL_HOST_USER=''
EMAIL_HOST_PASSWORD=''
ALLOWED_HOSTS=['*']


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'develop.db',
    }
}

MEDIA_URL='/media/'
MEDIA_ROOT = os.path.join(BASE_DIR,'media/') 
