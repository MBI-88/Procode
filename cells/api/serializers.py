from attr import fields
from rest_framework import serializers
from ..models import ShopingCellModel,ProfileUserModel
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


    def create(self, validated_data) -> object:
        user = User()
        user.username = validated_data['username']
        user.first_name = validated_data['first_name']
        user.last_name = validated_data['last_name']
        user.set_password(validated_data['password'])
        user.email = validated_data['email']
        user.save()
        ProfileUserModel.objects.create(user=user,phone=validated_data['phone'])
        return user


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
    
    
    def update(self, instance, validated_data) -> object:
        updated_user = validated_data['user']
        updated_user.username = validated_data['username']
        updated_user.first_name = validated_data['first_name']
        updated_user.last_name = validated_data['last_name']
        updated_user.email = validated_data['email']
        updated_user.profile = validated_data['phone']
        updated_user.profile = validated_data['image']
        updated_user.profile = validated_data['address']
        updated_user.save()
        updated_user.profile.save()
        return updated_user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','email','first_name','last_name']

class ProfileUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileUserModel
        fields = ['phone','address','image','created_date','updated_date']