from base_setting import *

DEBUG = False

SECRET_KEY =  b'django-secure-' + os.urandom(20)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = '' # Put your e-mail admin
EMAIL_PORT = '' # Put your port 
EMAIL_HOST_USER = 'procode@gmail.com'
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = True
EMAIL_USE_SSL = True

# Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'Procode',
        'USER': 'ProcodeAdmin',
        'HOST': '',
        'PORT': '',
        'PASSWORD': 'pr0c0d3*@dmin',
    }
}

