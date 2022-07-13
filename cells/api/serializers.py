from pyexpat import model
from attr import fields
from rest_framework.serializers import ModelSerializer
from ..models import ProfileUserModel,ShopingCellModel
from django.contrib.auth.models import User

# Serializer

class ProfileUserModelSerializer(ModelSerializer):
    class Meta:
        model = ProfileUserModel
        fields = ['user','phone','image','address']
    
class ShopingCellModelSerializer(ModelSerializer):
    class Meta:
        model = ShopingCellModel
        fields = ['owner_user','profile','model_name','price','image','description']

class UserModelSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email']