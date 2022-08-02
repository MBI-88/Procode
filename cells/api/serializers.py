from crypt import methods
from rest_framework import serializers
from ..models import ProfileUserModel,ShopingCellModel
from django.contrib.auth.models import User
import re

# Serializer
 
class ShopingCellModelListSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    model_name = serializers.CharField(max_length=150,required=True)
    updated_date = serializers.CharField(required=False)
    price = serializers.CharField(max_length=6,required=False)
    image = serializers.ImageField()
    description = serializers.CharField(max_length=1000,required=False)

    
    def userinstance(self,instance:object) -> object:
        self.user = instance
        print(self.user.username,' ',self.user.profile.phone)
        

    def create(self, validated_data) -> object:
        ShopingCellModel.objects.create(
            owner_user=self.user,
            profile=self.user.profile,
            model_name=validated_data['model_name'],
            price=validated_data['price'],
            image=validated_data['image'],
            description=validated_data['description']
        )

        return super().create(validated_data)
    
  



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
        user.is_active = True
        user.save()
        ProfileUserModel.objects.create(user=user,phone=validated_data['phone'])
        return super().create(validated_data)


class UserUpdateSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=25,required=False)
    first_name = serializers.CharField(max_length=50,required=False)
    last_name = serializers.CharField(max_length=100,required=False)
    email = serializers.EmailField()
    phone = serializers.CharField(max_length=8,required=True)
    created_date = serializers.DateTimeField(required=False)
    updated_date = serializers.DateTimeField(required=False)
    image = serializers.ImageField(required=False)
    address = serializers.CharField(max_length=200,required=False)


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
        return super().update(instance, validated_data)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email']

class ProfileUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileUserModel
        fields = ['phone','created_date','updated_date','image','address']