from rest_framework import serializers
from ..models import ShopingCellModel
from django.contrib.auth.models import User
import re

# Serializer
 
class ShopingCellModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopingCellModel
        fields = ['owner_user','profile','model_name','price','image','description']

class UserRegistrationSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=25,required=True)
    first_name = serializers.CharField(max_length=50,required=True)
    last_name = serializers.CharField(max_length=100,required=True)
    password = serializers.CharField(required=True)
    password2 = serializers.CharField(required=True)
    email = serializers.EmailField()
    phone = serializers.CharField(max_length=8,required=True)

    def validate_password2(self,value) -> str:
        if (self.context['password'] != value):
            raise serializers.ValidationError('Las claves no coinciden')
        
        return value
    
    def validate_phone(self,value) -> str:
        pattern = re.compile("^5[1-8]")   
        if (len(value) == 8):
            if (pattern.search(value)):
                return value
        raise serializers.ValidationError('El numero no coincide con el prefijo del sistema')


class UpdateUserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=25,required=True)
    first_name = serializers.CharField(max_length=50,required=True)
    last_name = serializers.CharField(max_length=100,required=True)
    email = serializers.EmailField()
    phone = serializers.CharField(max_length=8,required=True)
    image = serializers.ImageField()
    address = serializers.CharField(max_length=100,required=True)


    def validate_phone(self,value) -> str:
        pattern = re.compile("^5[1-8]")   
        if (len(value) == 8):
            if (pattern.search(value)):
                return value
        raise serializers.ValidationError('El numero no coincide con el prefijo del sistema')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','email','first_name','last_name']