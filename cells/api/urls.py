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
    path('profile/update/',apiviews.ProfileUpdate.as_view(),name='profile_update_api'),
    path('profile/delete/',apiviews.DeleteProfile.as_view(),name='profile_delete_api'),
    path('create/item/',apiviews.CreateItem.as_view(),name='create_item_api'),
    path('profile/change-password/',apiviews.ChangePassword.as_view(),name='change_password_api'),
    path('profile/changed-password/<uidb64>/<token>/',apiviews.ChangedPassword.as_view(),name='changed_password_api'),
    path('update/item/<int:pk>/',apiviews.UpdateItem.as_view(),name='update_item_api'),
    path('delete/item/<int:pk>/',apiviews.DeleteItem.as_view(),name='delete_item_api'),
    
]
