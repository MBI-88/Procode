from rest_framework.views import APIView
from ..models import ShopingCellModel
from .serializers import (ShopingCellModelListSerializer,UserRegistrationSerializer,
                          UserUpdateSerializer,UserSerializer)
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from django.contrib.sessions.models import Session 
from django.contrib.auth.models import User
from datetime import datetime
from rest_framework.pagination import PageNumberPagination
import re


# Views

# Login (Register) ok
class Login(ObtainAuthToken):
    authentication_classes = ()
    permission_classes = ()
    http_method_names = ['post']

    def post(self, request, *args, **kwargs) -> Response:
        login_s = self.serializer_class(data=request.data,context={'request':request})
        if login_s.is_valid():
            user = login_s.validated_data['user']
            user_s = UserSerializer(user)
            if user.is_active:
                token,created = Token.objects.get_or_create(user=user)
                if created:
                   return Response(
                    {'token':token.key,'user':user_s.data,'message':'Login ok!'},status=status.HTTP_201_CREATED)

                else:
                    token.delete()
                    return Response({'error':'User session already'},status=status.HTTP_409_CONFLICT)
            else: 
                return Response({'error':'User not actived'},status=status.HTTP_401_UNAUTHORIZED)
        return Response(data=login_s.errors, status=status.HTTP_406_NOT_ACCEPTABLE)


# Logout (Register) ok
class Logout(APIView):
    queryset = Session.objects.all()
    http_method_names = ['get']
    
    def get(self,request,*args, **kwargs) -> Response:
        try:
            token = request.auth
            if token is not None:
                token = Token.objects.filter(key=token).first()
                user = token.user
                all_sessions = self.queryset.filter(expire_date__gte=datetime.now())
                if all_sessions.exists():
                    for session in all_sessions:
                        session_data = session.get_decode()
                        if user.id == int(session_data.get('_auth_user_id')):
                            session.delete()
                token.delete()
                return Response({'Session':'Done!'},status=status.HTTP_200_OK)
            return Response({'error':'Not token'},status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({'message':'Token not exists'},status=status.HTTP_404_NOT_FOUND)
        


# Register (Register) pendiente
class Register(APIView):
    authentication_classes = ()
    permission_classes = ()
    http_method_names = ['post']

    def post(self,request:str,*args, **kwargs) -> Response:
        data = UserRegistrationSerializer(request.data)
        if data.is_valid():
            try:
                data.save()
                return Response(data={'message':'Registration done!'},status=status.HTTP_201_CREATED)
            except:
                return Response(data={'message':'Error'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(data=data.errors,status=status.HTTP_406_NOT_ACCEPTABLE)




# List Items (Dashboard) ok
class ShowItems(APIView):
    authentication_classes = ()
    permission_classes = ()
    queryset = ShopingCellModel.objects.all()
    serializer_class = ShopingCellModelListSerializer
    pagination_class = PageNumberPagination
    http_method_names = ['get']

    def get(self, request:str, *args, **kwargs) -> Response:
        search = request.GET.get('search')
        pattern = re.compile("[a-zA-Z0-9\s]+")
        page = request.GET.get('page')
        try:
            page = int(request.GET.get('page'))
        except:
            return Response({'message':'Page not integer'},status=status.HTTP_400_BAD_REQUEST)

        if search is not None and pattern.search(search):
            items = self.paginate_queryset(self.queryset.filter(model_name__icontains=search))
        else: items = self.paginate_queryset(self.queryset)
            
        if items is not None:
            serializer = self.serializer_class(items,many=True)
            return self.get_paginated_response(serializer.data)
            
    @property
    def paginator(self) -> object:
        if not hasattr(self,'_paginator'):
            if not hasattr(self, '_paginator'):
                if self.pagination_class is None:
                    self._paginator = None
                else:
                    self._paginator = self.pagination_class()
        return self._paginator  
    
    def paginate_queryset(self, queryset:object) -> object:
        if self.paginator is None:
            return None
        return self.paginator.paginate_queryset(queryset, self.request, view=self)
    
    def get_paginated_response(self, data:dict) -> Response:
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data)




# Detail item (Dashboar) ok
class DetailItem(APIView):
    authentication_classes = ()
    permission_classes = ()
    queryset = ShopingCellModel.objects.all()
    serializer_class = ShopingCellModelListSerializer
    http_method_names = ['get']

    def get(self,request:str, *args, **kwargs) -> Response:
        pk = kwargs['pk']
        item = self.queryset.get(pk=pk)
        user = {
            'first_name':item.owner_user.first_name,
            'email':item.owner_user.email,
            'phone':item.profile.phone,
        }
        user = UserUpdateSerializer(user)
        item = self.serializer_class(item)
        data = {
            'user_data':user.data,
            'item_data':item.data,
        }

        return Response(data=data,status=status.HTTP_200_OK)




# Create Item (Profile) ok
class CreateItem(APIView):
    serializer_class = ShopingCellModelListSerializer
    http_method_names = ['post']
    
    def post(self,request:str,*args, **kwargs) -> Response:
        token = request.auth
        if token is not None:
            token = Token.objects.filter(key=token).first()
            user = token.user
            data = self.serializer_class(data=request.data)
            data.userinstance(user)
            if data.is_valid():
                data.save()
                return Response({'message':'Item created!'},status=status.HTTP_201_CREATED)
            return Response({'message':data.errors},status=status.HTTP_406_NOT_ACCEPTABLE)
        return Response({'message':'Not credentials'},status=status.HTTP_401_UNAUTHORIZED)


# Update Item (Profile) ok
class UpdateItem(APIView):
    queryset = ShopingCellModel.objects.all()
    serializer_class = ShopingCellModelListSerializer
    http_method_names = ['put']

    def put(self,request:str,*args, **kwargs) -> Response:
        token = request.auth
        pk = kwargs['pk']
        if token is not None:
            user = token.user
            user_item = self.queryset.get(pk=pk)
            if user.username == user_item.owner_user.username:
                data = self.serializer_class(instance=user_item,data=request.data)
                if data.is_valid():
                    data.save()
                    return Response({'message':'Item updated!'},status=status.HTTP_202_ACCEPTED)
                return Response({'message':data.errors},status=status.HTTP_406_NOT_ACCEPTABLE)
            return Response({'message':'It\'s not your item'},status=status.HTTP_401_UNAUTHORIZED)
        return Response({'message':'Not credentials'},status=status.HTTP_401_UNAUTHORIZED)


# Delete Item (Profile) ok
class DeleteItem(APIView):
    queryset = ShopingCellModel.objects.all()
    http_method_names = ['delete']

    def delete(self,request:str,*args, **kwargs) -> Response:
        token = request.auth
        pk = kwargs['pk']
        if token is not None:
            user = token.user
            user_item = self.queryset.get(pk=pk)
            if user.username == user_item.owner_user.username:
                self.queryset.filter(pk=pk).delete()
                return Response({'message':'Item deleted!'},status=status.HTTP_200_OK)
            return Response({'message':'It\'s not your item'},status=status.HTTP_401_UNAUTHORIZED)
        return Response({'message':'Not credentials'},status=status.HTTP_401_UNAUTHORIZED)
    
    
    


# Show Items (Profile) ok
class ShowItemProfile(ShowItems):
    authentication_classes = (TokenAuthentication,)

    def get(self, request: str, *args, **kwargs) -> Response:
        search = request.GET.get('search')
        pattern = re.compile("[a-zA-Z0-9\s]+")
        page = request.GET.get('page')
        token = request.auth

        if token is not None:
            token = Token.objects.filter(key=token).first()
            user = token.user
            try:
                page = int(request.GET.get('page'))
            except:
                return Response({'message':'Page not integer'},status=status.HTTP_400_BAD_REQUEST)
            
            if search is not None and pattern.search(search):
                    items = self.paginate_queryset(self.queryset.filter(owner_user=user).filter(model_name__icontains=search))
            else: items = self.paginate_queryset(self.queryset.filter(owner_user=user))

            if items is not None:
                serializer = self.serializer_class(items,many=True)
                return self.get_paginated_response(serializer.data)
        
        return Response({'message':'Not token'},status=status.HTTP_400_BAD_REQUEST)



# Profile (Profile) ok
class Profile(APIView):
    serializer_class = UserUpdateSerializer
    http_method_names = ['get']
    
    def get(self,request:str,*args,**kwargs) -> Response:
        token = Token.objects.filter(key=request.auth).first()
        if token is not None:
            user = token.user
            user_data = {
                'username':user.username,
                'first_name':user.first_name,
                'last_name':user.last_name,
                'email':user.email,
                'phone':user.profile.phone,
                'created_date':user.profile.created_date,
                'updated_date':user.profile.updated_date,
                'image':user.profile.image,
                'address':user.profile.address
            }
            user_data = self.serializer_class(user_data)
            return Response(data=user_data.data,status=status.HTTP_200_OK)
        return Response({'message':'Not token'},status=status.HTTP_400_BAD_REQUEST)



# Profile Update (Profile)
class ProfileUpdate(APIView):
    http_method_names = ['put']

    def put(self,request:str,*args, **kwargs) -> Response:
        token = request.auth

        if token is not None:
            token = Token.objects.filter(key=token).first()
            user_s = UserUpdateSerializer(instance=token.user,data=request.data)
            if user_s.is_valid():
                user_s.save()
                return Response({'message':'Profile updated!'},status=status.HTTP_201_CREATED) 

            return Response({'error':user_s.errors},status=status.HTTP_406_NOT_ACCEPTABLE)   

        return Response({'message':'Not token'},status=status.HTTP_401_UNAUTHORIZED)



# Profile Delete (Profile)
class DeleteProfile(APIView):
    http_method_names = ['delete']

    def delete(self,request:str,*args, **kwargs) -> Response:
        token = request.auth
        if token is not None:
            token = Token.objects.get(key=token)
            user = token.user
            User.objects.filter(username=user.username).delete()
        return Response({'message':'User deleted!'},status=status.HTTP_202_ACCEPTED)


# Profile Change password (Profile)
class ChangePassword(APIView):
    pass


# Profile Changed password (Profile)
class ChangedPassword(APIView):
    pass
    