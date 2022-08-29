from base_setting import *

DEBUG = True

SECRET_KEY = 'django-insecure'
EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'
EMAIL_HOST = 'localhost'
EMAIL_PORT = '1025'

# Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'test.db',
    }
}
