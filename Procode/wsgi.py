import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Procode.settings.production_setting')

application = get_wsgi_application()
