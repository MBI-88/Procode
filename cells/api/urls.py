from django.urls import path
from . import apiviews

app_name = 'cells_api'

urlpatterns = [
    path('login/',apiviews.Login.as_view(),name='login_api'),
    path('logout/',apiviews.Logout.as_view(),name='logout_api'),
    path('register/',apiviews.Register.as_view(),name='register_api'),
    path('showitems/',apiviews.ShowItems.as_view(),name='showitems_api'),
    path('detail/item/<int:pk>/',apiviews.DetailItem.as_view(),name='detail_item_api'),
    path('profile/',apiviews.Profile.as_view(),name='profile_api'),
    path('profile/showitems/',apiviews.ShowItemProfile.as_view(),name='profile_showitems_api'),
    path('itemprofile/',apiviews.ItemProfile.as_view(),name='item_profile_api'),
    path('profile/change-password/',apiviews.ChangePassword.as_view(),name='change_password_api'),
    path('profile/changed-password/<uidb64>/<token>/',apiviews.ChangedPassword.as_view(),name='changed_password_api'),

]
