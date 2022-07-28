from rest_framework import serializers
from ..models import ShopingCellModel,ProfileUserModel
from django.contrib.auth.models import User
import re

# Serializer
 
class ShopingCellModelListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopingCellModel
        fields = ['model_name','owner_user','profile','updated_date','price','image','description']


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


class UserUpdateSerializer(serializers.Serializer):
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
        instance.username = validated_data['username']
        instance.first_name = validated_data['first_name']
        instance.last_name = validated_data['last_name']
        instance.email = validated_data['email']
        instance.profile.phone = validated_data['phone']
        instance.profile.image = validated_data['image']
        instance.profile.address = validated_data['address']
        instance.save()
        instance.profile.save()
        return instance


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','email','first_name','last_name']

class ProfileUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileUserModel
        fields = ['phone','address','image','created_date','updated_date']