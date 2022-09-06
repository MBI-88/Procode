"""Procode URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import handler403,handler500,handler404,handler400

urlpatterns = [
    path('pr0c0d3-admin/', admin.site.urls),
    path('cells/',include('cells.urls',namespace='cells')),
    path('api/',include('cells.api.urls',namespace='cells_api')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

handler400 = 'cells.views.page_400_bad_request'
handler403 = 'cells.views.page_403_not_acces'
handler404 = 'cells.views.page_404_not_found'
handler500 = 'cells.views.page_500_error'