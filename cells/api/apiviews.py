from rest_framework.views import APIView
from ..models import ShopingCellModel
from .serializers import (ProfileUserSerializer, ShopingCellModelListSerializer,
                          UserRegistrationSerializer,UserUpdateSerializer,UserSerializer)
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.sessions.models import Session 
from datetime import datetime
from rest_framework.pagination import PageNumberPagination
import re


# Views

# Login (Register)
class Login(ObtainAuthToken):
    
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
                return Response({'error':'Not starting session'},status=status.HTTP_401_UNAUTHORIZED)
        return Response(data=login_s.errors, status=status.HTTP_400_BAD_REQUEST)


class Logout(APIView):
    
    def get(self,request,*args, **kwargs) -> Response:
        try:
            token = request.GET.get('token')
            token = Token.objects.filter(key=token).first()
            if token:
                user = token.user
                all_sessions = Session.objects.filter(expire_date__gte=datetime.now())
                if all_sessions.exists():
                    for session in all_sessions:
                        session_data = session.get_decode()
                        if user.id == int(session_data.get('_auth_user_id')):
                            session.delete()

                token.delete()
                return Response({'Session':'Done!'},status=status.HTTP_200_OK)

            return Response({'error':'Not user credentials'},status=status.HTTP_400_BAD_REQUEST)
        
        except:
            return Response({'error':'Not token'},status=status.HTTP_409_CONFLICT) 
        


# Register (Register)
class Register(APIView):
    
    def post(self,request:str,*args, **kwargs) -> Response:
        data = UserRegistrationSerializer(request.data)
        if data.is_valid():
            try:
                data.save()
                return Response(data={'message':'Registration done!'},status=status.HTTP_201_CREATED)
            except:
                return Response(data={'message':'Error'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(data=data.error_messages,status=status.HTTP_406_NOT_ACCEPTABLE)




# List Items (Dashboard)
class ShowItems(APIView):
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
    

    def get_paginated_response(self, data:dict) -> object:
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data)
    


    




# Create Item (Profile)
class CreateItem():
    pass


# Update Item (Profile)
class UpdateItem():
    pass


# Delete Item (Profile)
class DeleteItem():
    pass


# Profile (Profile)
class Profile(ShowItems):
    permission_classes = IsAuthenticated
    queryset = ShopingCellModel.objects.all()
    serializer_class = ShopingCellModelListSerializer
    pagination_class = PageNumberPagination
    
    def get(self,request:str,*args, **kwargs) -> Response:
        search = request.GET.get('search')
        pattern = re.compile("[a-zA-Z0-9\s]+")
        page = request.GET.get('page')
        token = request.GET.get('token')
        token = Token.objects.filter(key=token).first()

        if token:
            user = token.user
            try:
                page = int(request.GET.get('page'))
            except:
                return Response({'message':'Page not integer'},status=status.HTTP_400_BAD_REQUEST)

            if search is not None and pattern.search(search):
                items = self.paginate_queryset(self.queryset.filter(owner_user=user).filter(model_name__icontains=search))
            else: items = self.paginate_queryset(self.queryset.filter(owner_user=user))
                
            if items is not None:
                data_items_s = self.serializer_class(items,many=True)
                user_data_s = UserSerializer(user)
                profile_data_s = ProfileUserSerializer(user.profile)
            
                return Response({'user':user_data_s,'profile':profile_data_s,'items':data_items_s},status=status.HTTP_200_OK)
        
        return Response({'message':'Not token'},status=status.HTTP_400_BAD_REQUEST)

        
    
    


# Profile Update (Profile)
class ProfileUpdate(APIView):
    permission_classes = IsAuthenticated
    
    def post(self,request:str,*args, **kwargs) -> Response:
        token = request.POST.get('token')
        token = Token.objects.filter(key=token).first()
        if token:
            user_s = UserUpdateSerializer(instance=token.user,data=request.data)
            if user_s.is_valid():
                user_s.save()
                return Response({'message':'Profile updated','user':user_s.data},
                                status=status.HTTP_200_OK) 

            return Response({'message':'Not valid credential'},
                            status=status.HTTP_409_CONFLICT)   

        return Response({'message':'Not token'},status=status.HTTP_401_UNAUTHORIZED)



# Profile Delete (Profile)
class DeleteProfile():
    pass