from pathlib import Path
import os
from decouple import config
import cloudinary
import cloudinary_storage


BASE_DIR = Path(__file__).resolve().parent.parent

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cloudinary',
    'cloudinary_storage',
    'cells.apps.CellsConfig',
    'widget_tweaks',
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'whitenoise.runserver_nostatic',
    
]

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES':[
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES':[
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PAGINATION_CLASS':'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE':15
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    
]

CORS_ORIGIN_WHITELIST = (
    'http://localhost:3000','http://localhost:8000'
)

ROOT_URLCONF = 'procode.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'procode.wsgi.application'

# Password validation

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

# Static files (CSS, JavaScript, Images)

STATIC_URL = 'static/'

# Cloudinary stuff
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': config('CLOUD_NAME', default=""),
    'API_KEY': config('API_KEY', default=""),
    'API_SECRET': config('API_SECRET', default=""),
    'MEDIA_TAG': config('MEDIA_TAG',default=""),
    'STATIC_IMAGES_EXTENSIONS': config('STATIC_IMAGES_EXTENSIONS', lambda v:[s.strip() for s in v.split(',')])
}

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# Internationalization

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Default primary key field type

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Redirect Urls

LOGING_REDIRECT_URL = 'cells:profile'
LOGOUT_REDIRECT_URL = 'cells:index'
LOGIN_URL = 'cells:login'
LOGOUT_URL = 'cells:logout'

# Time delay

PASSWORD_RESET_TIMEOUT_DAYS = 86400 #s

