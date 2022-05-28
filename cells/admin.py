from django.contrib import admin
from .models import ShopingCell,ProfileUser

# Register your models here.

@admin.register(ShopingCell)
class ShopingCellAdmin(admin.ModelAdmin):
    pass

@admin.register(ProfileUser)
class ProfileUserAdmin(admin.ModelAdmin):
    pass