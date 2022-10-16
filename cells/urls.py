from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

app_name = 'cells'

# urlpatterns

urlpatterns = [ 
    path('index/',views.index,name='index'),
    path('login/',views.LoginUser.as_view(),name='login'),
    path('logout/',LogoutView.as_view(),name='logout'),
    path('register/',views.Register.as_view(),name='register'),
    path('register/changepassword/',views.ChangePasswordProfile.as_view(),name='change_password'),
    path('register/<uidb64>/<token>/',views.tokenLinkRecived,name='token_link'),
    path('restore/password/',views.RestorePassword.as_view(),name='restore_password'),
    path('shopping/',views.ShowItems.as_view(),name='dashboar_list'),
    path('shopping/<int:pk>/',views.DetailItem.as_view(),name='dashboar_detail'),
    path('create/item/',views.CreateItem.as_view(),name='create_item'),
    path('update/item/<int:pk>/',views.UpdateItem.as_view(),name='update_item'),
    path('delete/item/<int:pk>/',views.DeleteItem.as_view(),name='delete_item'),
    path('profile/',views.Profile.as_view(),name='profile'),
    path('update/profile/',views.UpdateProfile.as_view(),name='update_profile'),
    path('delete/profile/',views.DeleteProfile.as_view(),name='delete_profile'),
]