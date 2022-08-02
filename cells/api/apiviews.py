from rest_framework.views import APIView
from ..models import ShopingCellModel
from .serializers import (ProfileUserSerializer, ShopingCellModelListSerializer,
                          UserRegistrationSerializer,UserUpdateSerializer,UserSerializer)
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from django.contrib.sessions.models import Session 
from datetime import datetime
from rest_framework.pagination import PageNumberPagination
import re


# Views

# Login (Register) ok
class Login(ObtainAuthToken):
    authentication_classes = ()
    permission_classes = ()
    
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
    
    def get(self,request,*args, **kwargs) -> Response:
        try:
            token = request.auth
            token = Token.objects.filter(key=token).first()
            if token:
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
            pass
        


# Register (Register) pendiente
class Register(APIView):
    authentication_classes = ()
    permission_classes = ()

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




# Create Item (Profile)
class CreateItem(APIView):
    serializer_class = ShopingCellModelListSerializer
    
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


# Update Item (Profile)
class UpdateItem(APIView):
    
    def post(self,request:str,*args, **kwargs) -> Response:
        token = request.auth
        return


# Delete Item (Profile)
class DeleteItem(APIView):
    
    def post(self,request:str,*args, **kwargs) -> Response:
        token = request.auth
        return


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
    
    def get(self,request:str,*args,**kwargs) -> Response:
        token = Token.objects.filter(key=request.auth).first()

        if token:
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
    
    def post(self,request:str,*args, **kwargs) -> Response:
        token = request.auth
        token = Token.objects.filter(key=token).first()
        if token:
            user_s = UserUpdateSerializer(instance=token.user,data=request.data)
            if user_s.is_valid():
                user_s.save()
                return Response({'message':'Profile updated!'},status=status.HTTP_200_OK) 

            return Response({'message':'Invalid credential','error':user_s.errors},
                            status=status.HTTP_406_NOT_ACCEPTABLE)   

        return Response({'message':'Not token'},status=status.HTTP_401_UNAUTHORIZED)



# Profile Delete (Profile)
class DeleteProfile(APIView):

    def post(self,request:str,*args, **kwargs) -> Response:
        token = request.auth
        return


# Profile Change password (Profile)
class ChangePassword(APIView):
    pass


# Profile Changed password (Profile)
class ChangedPassword(APIView):
    pass
    