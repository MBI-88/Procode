from .base_setting import *

# User name: Procode password: pr0c0d3 email:procode@gmail.com
DEBUG = True

SECRET_KEY = 'django-insecure-tx^m7&!dk1pdfri*+roe+2-&#^^x-cph^aknzv60l9x&dwxbkc'
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST = 'localhost'
EMAIL_PORT = '1025'

# Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'develop.db',
    }
}

# Media file (user images, cells images,etc)

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR,'media/') 
