from sys import maxsize
from rest_framework import serializers
from ..models import ProfileUserModel,ShopingCellModel
from django.contrib.auth.models import User
import re

# Serializer

 #*********************** Items **********************************************************

class ShopingCellModelListSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    model_name = serializers.CharField(max_length=150,required=True)
    updated_date = serializers.CharField(required=False)
    price = serializers.CharField(max_length=6,required=False)
    image = serializers.ImageField(allow_null=True) # validate on front end image type (jpg,png)
    description = serializers.CharField(max_length=1000,required=False,allow_null=True)

    def userinstance(self,instance:object) -> object:
        self.user = instance
        
    def create(self, validated_data:dict) -> object:
        ShopingCellModel.objects.create(
            owner_user=self.user,
            profile=self.user.profile,
            model_name=validated_data['model_name'],
            price=validated_data['price'],
            image=validated_data['image'],
            description=validated_data['description']
        )
        return validated_data
    
    def update(self, instance:object, validated_data:dict) -> object:
        ShopingCellModel.objects.filter(pk=instance.pk).update(
            model_name=validated_data['model_name'],
            price=validated_data['price'],
            image=validated_data['image'],
            description=validated_data['description']
        )
        return instance
    

#******************************* User ************************************************************

class UserRegistrationSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=25,required=True)
    first_name = serializers.CharField(max_length=50,required=True)
    last_name = serializers.CharField(max_length=100,required=True)
    password = serializers.CharField(required=True,max_length=50)
    password2 = serializers.CharField(required=True,max_length=50)
    email = serializers.EmailField(max_length=50,required=True)
    phone = serializers.CharField(max_length=8,required=True)

    def validate(self, attrs:dict) -> dict:
        pattern = re.compile("^5[1-8]")
        if attrs['password'] != attrs['password2']: raise serializers.ValidationError('Password not mach')
        if (len(attrs['phone']) != 8 and pattern.search(attrs['phone']) == None):
            raise serializers.ValidationError('Phone number not valid')
        return attrs

    def create(self, validated_data:dict) -> object:
        if User.objects.filter(email=validated_data['email']).exists():
            raise serializers.ValidationError('E-mail already exists')
        user = User()
        user.username = validated_data['username']
        user.first_name = validated_data['first_name']
        user.last_name = validated_data['last_name']
        user.set_password(validated_data['password'])
        user.email = validated_data['email']
        user.is_active = False
        try:
            user.save()
            ProfileUserModel.objects.create(user=user,phone=validated_data['phone'])
        except:
            raise serializers.ValidationError('User already exists')
        return validated_data


class UserUpdateSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=25,required=True)
    first_name = serializers.CharField(max_length=50,required=True)
    last_name = serializers.CharField(max_length=100,required=True)
    email = serializers.EmailField(max_length=50,required=True)
    phone = serializers.CharField(max_length=8,required=True)
    created_date = serializers.DateTimeField(required=False)
    updated_date = serializers.DateTimeField(required=False)
    image = serializers.ImageField(required=False,allow_null=True) # validate on front end image type (jpg,png)
    address = serializers.CharField(max_length=200,required=False)

    def validate_phone(self,value:str) -> str:
        pattern = re.compile("^5[1-8]")   
        if (len(value) == 8) and pattern.search(value):
            return value
        raise serializers.ValidationError('The phone number not match')
    
    def update(self, instance:object, validated_data:dict) -> object:
        instance.username = validated_data['username']
        instance.first_name = validated_data['first_name']
        instance.last_name = validated_data['last_name']
        if instance.email == validated_data['email']: pass
        else:
            if User.objects.filter(email=validated_data['email']).exists():
                raise serializers.ValidationError('E-mail already exists')
            instance.email = validated_data['email']
        instance.is_active = False
        instance.profile.phone = validated_data['phone']
        instance.profile.image = validated_data['image']
        instance.profile.address = validated_data['address']
        try:
            instance.save()
            instance.profile.save()
        except:
            raise serializers.ValidationError('The username already exists')
        return instance


class ProfileSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=50,required=True)
    last_name = serializers.CharField(max_length=100,required=True)
    phone = serializers.CharField(max_length=8,required=True)



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email']


class UserChangePassSerializer(serializers.Serializer):
    currentpassword = serializers.CharField(required=True,max_length=50)
    newpassword = serializers.CharField(required=True,max_length=50)
    confirmpassword = serializers.CharField(required=True,max_length=50)

    def validate(self, attrs:dict) -> dict:
        if (attrs['currentpassword'] == attrs['newpassword']):
            raise serializers.ValidationError('Current password equal to  new password')
        if (attrs['newpassword'] != attrs['confirmpassword']):
            raise serializers.ValidationError('Passwords not mach')
        return attrs
    
    def update(self, instance:object, validated_data:dict) -> object:
        instance.set_password(validated_data['newpassword'])
        instance.is_active = False
        instance.save()
        return instance


class UserRestorePasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True,max_length=50)

    def update(self, instance:object, validated_data:dict) -> object:
        instance.is_active = False
        instance.set_password('password1') # hacerlo mas fuerte para producción
        instance.save()
        return instance