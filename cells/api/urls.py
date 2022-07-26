from django.urls import path
from . import views

app_name = 'cells_api'

urlpatterns = [
    path('login/',views.Login.as_view(),name='login_api'),
    path('logout/',views.Logout.as_view(),name='logout_api'),
    path('register/',views.Register.as_view(),name='register_api'),
    path('showitems/',views.ShowItems.as_view(),name='showitems_api'),
    path('showitem/<int:pk>/',views.DetailItem.as_view(),name='detailitem_api'),
]
