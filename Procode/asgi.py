import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'procode.settings.develop_setting')

application = get_asgi_application()
