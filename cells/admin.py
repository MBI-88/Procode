from django.contrib import admin
from .models import ShopingCell,ProfileUser

admin.site.site_header = 'ProC0d3 Control'
admin.site.index_title = 'ProC0d3 admin'

# Register your models here.

@admin.register(ShopingCell)
class ShopingCellAdmin(admin.ModelAdmin):
    list_display = ['model_name','created_date','price','updated_date']
    list_filter = ['updated_date']
    ordering = ['-updated_date']
    fields = ['model_name','price']
    search_fields = ['model_name','price']

@admin.register(ProfileUser)
class ProfileUserAdmin(admin.ModelAdmin):
    list_display = ['phone','address','created_date']
    list_filter = ['created_date']
    search_fields = ['phone']