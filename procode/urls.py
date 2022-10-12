from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import handler403, handler500, handler404, handler400

urlpatterns = [
    path('pr0c0d3-admin/', admin.site.urls),
    path('cells/', include('cells.urls', namespace='cells')),
    path('api/', include('cells.api.urls', namespace='cells_api')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
else:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

handler400 = 'cells.views.page_400_bad_request'
handler403 = 'cells.views.page_403_not_acces'
handler404 = 'cells.views.page_404_not_found'
handler500 = 'cells.views.page_500_error'
