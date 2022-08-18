import email
from urllib import request
from rest_framework.views import APIView
from ..models import ShopingCellModel
from .serializers import (ShopingCellModelListSerializer, UserChangePassSerializer,UserRegistrationSerializer,
                          UserUpdateSerializer,UserSerializer,UserRestorePasswordSerializer)
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from django.contrib.sessions.models import Session 
from django.contrib.auth.models import User
from datetime import datetime
from rest_framework.pagination import PageNumberPagination
from cells.views import sendEmail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes,force_str
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator
import re


# Views
# ****************************************** Login Views **************************************

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
                    {'token':token.key,'user':user_s.data,'message':'Login ok!'},status=status.HTTP_202_ACCEPTED)
                else:
                    token.delete()
                    return Response({'error':'User session exists'},status=status.HTTP_409_CONFLICT)
            else: 
                return Response({'error':'User not actived'},status=status.HTTP_401_UNAUTHORIZED)
        return Response(data=login_s.errors, status=status.HTTP_406_NOT_ACCEPTABLE)


# Logout (Register) ok
class Logout(APIView):
    queryset = Session.objects.all()
    http_method_names = ['get']
    
    def get(self,request,*args, **kwargs) -> Response:
        try:
            token = Token.objects.get(key=request.auth)
            if token is not None:
                user = token.user
                all_sessions = self.queryset.filter(expire_date__gte=datetime.now())
                if all_sessions.exists():
                    for session in all_sessions:
                        session_data = session.get_decode()
                        if user.id == int(session_data.get('_auth_user_id')):
                            session.delete()
                token.delete()
                return Response({'Session':'Done!'},status=status.HTTP_200_OK)
            return Response({'error':'Not token'},status=status.HTTP_406_NOT_ACCEPTABLE)
        except:
            return Response({'message':'Token not exists'},status=status.HTTP_404_NOT_FOUND)
        

# ***************************************** Register View *******************************************

# Register (Register) ok
class Register(APIView):
    authentication_classes = ()
    permission_classes = ()
    http_method_names = ['post']
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer

    def post(self,request:str,*args, **kwargs) -> Response:
        data = self.serializer_class(data=request.data)
        if data.is_valid():
            data.save()
            new_user = self.queryset.get(username=request.data['username'])
            subject = 'ProC0d3 Api Registro de usuario' 
            # pendiente a cambios en la dirección de retorno (espera por front end)
            message = render_to_string('email/email_register_api.html',{
                'domain': get_current_site(request),
                'user': new_user.username,
                'uid': urlsafe_base64_encode(force_bytes(new_user.pk)),
                'token': default_token_generator.make_token(new_user),
                'protocol': request.scheme,
            })
            sendEmail(subject,message,new_user.email,new_user.username)
            return Response(data={'message':'Registration done, open your e-mail and fallow the link'},status=status.HTTP_201_CREATED)
        return Response(data=data.errors,status=status.HTTP_406_NOT_ACCEPTABLE)


#**************************************** Dashboard Views ******************************************

# List Items (Dashboard) ok
class ShowItems(APIView):
    authentication_classes = ()
    permission_classes = ()
    queryset = ShopingCellModel.objects.all()
    serializer_class = ShopingCellModelListSerializer
    pagination_class = PageNumberPagination
    http_method_names = ['get']

    def get(self, request:str, *args, **kwargs) -> Response:
        search = request.query_params.get('search')
        pattern = re.compile("[a-zA-Z0-9\s]+")
        page = request.query_params.get('page')
        try:
            page = int(page)
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



#*************************************** Profile Views ***************************************************

# Create Item (Profile) ok
class ItemProfile(APIView):
    serializer_class = ShopingCellModelListSerializer
    queryset = ShopingCellModel.objects.all()
    http_method_names = ['post','put','delete']
    
    def post(self,request:str,*args, **kwargs) -> Response:
        token = Token.objects.get(key=request.auth)
        if token is not None:
            user = token.user
            data = self.serializer_class(data=request.data)
            data.userinstance(user)
            if data.is_valid():
                data.save()
                return Response({'message':'Item created!'},status=status.HTTP_201_CREATED)
            return Response({'message':data.errors},status=status.HTTP_406_NOT_ACCEPTABLE)
        return Response({'message':'Not token'},status=status.HTTP_401_UNAUTHORIZED)
    
    def put(self,request:str,*args, **kwargs) -> Response:
        token = Token.objects.get(key=request.auth)
        pk = request.query_params.get('pk')
        if token is not None and pk is not None:
            user = token.user
            user_item = self.queryset.get(pk=pk)
            if user.username == user_item.owner_user.username:
                data = self.serializer_class(instance=user_item,data=request.data)
                if data.is_valid():
                    data.save()
                    return Response({'message':'Item updated!'},status=status.HTTP_202_ACCEPTED)
                return Response({'message':data.errors},status=status.HTTP_406_NOT_ACCEPTABLE)
            return Response({'message':'It\'s not your item'},status=status.HTTP_401_UNAUTHORIZED)
        return Response({'message':'Not credentials or id didn\t send'},status=status.HTTP_401_UNAUTHORIZED)
    
    def delete(self,request:str,*args, **kwargs) -> Response:
        token = Token.objects.get(key=request.auth)
        pk = request.query_params.get('pk')
        if token is not None and pk is not None:
            user = token.user
            user_item = self.queryset.get(pk=pk)
            if user.username == user_item.owner_user.username:
                self.queryset.filter(pk=pk).delete()
                return Response({'message':'Item deleted!'},status=status.HTTP_202_ACCEPTED)
            return Response({'message':'It\'s not your item'},status=status.HTTP_401_UNAUTHORIZED)
        return Response({'message':'Not credentials or id didn\t send'},status=status.HTTP_401_UNAUTHORIZED)


# Show Items (Profile) ok
class ShowItemProfile(ShowItems):
    authentication_classes = (TokenAuthentication,)

    def get(self, request: str, *args, **kwargs) -> Response:
        search = request.query_params.get('search')
        pattern = re.compile("[a-zA-Z0-9\s]+")
        page = request.query_params.get('page')
        token = Token.objects.get(key=request.auth)

        if token is not None:
            user = token.user
            try:
                page = int(page)
            except:
                return Response({'message':'Page not integer'},status=status.HTTP_400_BAD_REQUEST)
            
            if search is not None and pattern.search(search):
                    items = self.paginate_queryset(self.queryset.filter(owner_user=user).filter(model_name__icontains=search))
            else: items = self.paginate_queryset(self.queryset.filter(owner_user=user))

            if items is not None:
                serializer = self.serializer_class(items,many=True)
                return self.get_paginated_response(serializer.data)
        
        return Response({'message':'Not token'},status=status.HTTP_401_UNAUTHORIZED)



# Profile (Profile) ok
class Profile(APIView):
    serializer_class = UserUpdateSerializer
    http_method_names = ['get','put','delete']
    queryset = User.objects.all()
    
    def get(self,request:str,*args,**kwargs) -> Response:
        token = Token.objects.get(key=request.auth)
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
        return Response({'message':'Not token'},status=status.HTTP_401_UNAUTHORIZED)

    def put(self,request:str,*args, **kwargs) -> Response:
        token = Token.objects.get(key=request.auth)
        if token is not None:
            user_s = self.serializer_class(instance=token.user,data=request.data)
            if user_s.is_valid():
                user_s.save()
                subject = 'ProC0d3 Api Actualizacion de usuario de usuario' 
                # pendiente a cambios en la dirección de retorno (espera por front end)
                message = render_to_string('email/email_profile_api.html',{
                    'domain': get_current_site(request),
                    'user': user_s.username,
                    'uid': urlsafe_base64_encode(force_bytes(user_s.pk)),
                    'token': default_token_generator.make_token(user_s),
                    'protocol': request.scheme,
                })
                sendEmail(subject,message,user_s.email,user_s.username)
                return Response({'message':'Profile updated, open your e-mail and follow the link'},status=status.HTTP_202_ACCEPTED) 
            return Response({'error':user_s.errors},status=status.HTTP_406_NOT_ACCEPTABLE)   
        return Response({'message':'Not token'},status=status.HTTP_401_UNAUTHORIZED)
    
    def delete(self,request:str,*args, **kwargs) -> Response:
        token = Token.objects.get(key=request.auth)
        if token is not None:
            user = token.user
            self.queryset.filter(username=user.username).delete()
            return Response({'message':'User deleted!'},status=status.HTTP_202_ACCEPTED)
        return Response({'message':'Not token'},status=status.HTTP_401_UNAUTHORIZED)



# Profile Change password (Profile) ok
class ChangePassword(APIView):
    http_method_names = ['put']
    serializer_class = UserChangePassSerializer

    def put(self,request:str,*args, **kwargs) -> Response:
        token = Token.objects.get(key=request.auth)
        if token is not None:
            new_user = token.user
            data = self.serializer_class(instance=new_user,data=request.data)
            if data.is_valid():
                data.save()
                subject = 'ProC0d3 Api Registro de usuario' 
                # pendiente a cambios en la dirección de retorno (espera por front end)
                message = render_to_string('email/email_password_api.html',{
                    'domain': get_current_site(request),
                    'user': new_user.username,
                    'uid': urlsafe_base64_encode(force_bytes(new_user.pk)),
                    'token': default_token_generator.make_token(new_user),
                    'protocol': request.scheme,
                })
                sendEmail(subject,message,new_user.email,new_user.username)
                return Response({'message':'Open your e-mail and follow the link'},status=status.HTTP_200_OK)
            return Response({'message':'Invalid data'},status=status.HTTP_406_NOT_ACCEPTABLE)
        return Response({'message':'Not token'},status=status.HTTP_401_UNAUTHORIZED)


# Profile Changed password (Profile) pendiente
class TokenLinkRecived(APIView):
    http_method_names = ['get']
    authentication_classes = ()
    permission_classes = ()
    queryset = User.objects.all()

    def get(self,request:str, *args, **kwargs) -> Response:
        try:
            uid = force_str(urlsafe_base64_decode(args['uidb64']))
            user = self.queryset.get(pk=uid)
        except (TypeError,ValueError,OverflowError,User.DoesNotExist):
            user = None
        if (user is not None and default_token_generator.check_token(user,args['token'])):
            user.is_active = True
            user.save()
        else:
            return Response({'message':'User not exists'},status=status.HTTP_404_NOT_FOUND)
        return Response({'message':'Ok'},status=status.HTTP_202_ACCEPTED)

# Profile Restore password (Profile) pendiente
class RestorePassword(APIView):
    http_method_names = ['post']
    queryset = User.objects.all()
    authentication_classes = ()
    permission_classes = ()
    serializer_class = UserRestorePasswordSerializer

    def post(self,request:str,*args, **kwargs) -> Response:
        email = request.data['email'] # comprobar dato
        if email is not None:
            user = self.queryset.filter(email=email).first()
            if user is not None:
                data = self.serializer_class(instance=user,data=request.data)
                if data.is_valid():
                    data.save()
                    subject = 'ProC0d3 Api Registro de usuario' 
                    # pendiente a cambios en la dirección de retorno (espera por front end)
                    message = render_to_string('email/email_restored_api.html',{
                        'domain': get_current_site(request),
                        'user': user.username,
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': default_token_generator.make_token(user),
                        'protocol': request.scheme,
                        'password': 'password1',
                    })
                    sendEmail(subject,message,user.email,user.username)
                    return Response({'message':'Open your e-mail and follow the link'},status=status.HTTP_202_ACCEPTED)
            else:
                return Response({'message':'User not exists'},status=status.HTTP_404_NOT_FOUND)
        return Response({'message':'Email empty'},status=status.HTTP_406_NOT_ACCEPTABLE)

    