from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('pr0c0d3-admin/', admin.site.urls),
    path('cells/',include('cells.urls',namespace='cells')),
    path('api/',include('cells.api.urls',namespace='cells_api')),
]
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

