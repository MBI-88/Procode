from django.urls import path
from . import apiviews
from rest_framework.routers import DefaultRouter

routers = DefaultRouter()
app_name = 'cells_api'
routers.register('api',apiviews.ShowItems,basename='showitems')

urlpatterns = [
    path('login/',apiviews.Login.as_view(),name='login_api'),
    path('logout/',apiviews.Logout.as_view(),name='logout_api'),
    path('register/',apiviews.Register.as_view(),name='register_api'),
    
   
]
urlpatterns += routers.urls
