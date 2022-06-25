from django.urls import path
from . import views

app_name = 'cells'

# urlpatterns

urlpatterns = [ 
    path('index/',views.index,name='index'),
    path('login/',views.LoginUser.as_view(),name='login'),
    path('logout/',views.LoggedoutUser.as_view(),name='logout'),
    path('register/',views.RegisterUser.as_view(),name='register'),
    path('registrer/<uid64>/<token>/',views.registrationUserDone,name='registerdone'),
    path('reset/',views.ResetUserPassword.as_view(),name='password_reset'),
    path("reset/done/",views.PasswordResetDoneView.as_view(),name='password_reset_done'),
    path('reset/<uiid64>/<token>/',views.ResetUserPasswordConfirm.as_view(),name='password_reset_confirm'),
    path('reset/complete/',views.ResetUserPasswordComplete.as_view(),name='password_reset_complete'),
    path('shoping/',views.ShowItems.as_view(),name='dashboar_list'),
    path('shoping/<pk>/',views.DetailItem.as_view(),name='dashboar_detail'),
    path('create/item/',views.CreateItem.as_view(),name='create_item'),
    path('update/item/<pk>/',views.UpdateItem.as_view(),name='update_item'),
    path('delete/item/<pk>/',views.DeleteItem.as_view(),name='delete_item'),
    path('profile/',views.ProfileUser.as_view(),name='profile'),
    path('update/profile/<pk>/',views.UpdateProfile.as_view(),name='update_profile'),
    path('delete/profile/<pk>/',views.DeleteProfileUser.as_view(),name='delete_profile'),
]