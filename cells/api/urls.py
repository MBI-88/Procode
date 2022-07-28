from django.urls import path
from . import apiviews

app_name = 'cells_api'

urlpatterns = [
    path('login/',apiviews.Login.as_view(),name='login_api'),
    path('logout/',apiviews.Logout.as_view(),name='logout_api'),
    path('register/',apiviews.Register.as_view(),name='register_api'),
    path('showitems/',apiviews.ShowItems.as_view(),name='showitems_api'),
]
