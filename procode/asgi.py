import os
from django.core.asgi import get_asgi_application

<<<<<<< HEAD
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'procode.settings.develop_setting')
=======
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'procode.settings.production_setting')
>>>>>>> production

application = get_asgi_application()
