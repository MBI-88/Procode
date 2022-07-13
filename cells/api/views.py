from lib2to3.pgen2.token import tok_name
from rest_framework.views import APIView
from ..models import ProfileUserModel,ShopingCellModel
from django.contrib.auth.models import User
from .serializers import ShopingCellModelSerializer,UserRegistrationSerializer,UpdateUserSerializer 
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework import status
from rest_framework.authtoken.models import Token
from .serializers import UserSerializer,UserRegistrationSerializer,UpdateUserSerializer
from django.contrib.sessions.models import Session 
from datetime import datetime

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
                    return Response({'error':'Usuario ya inició session'},status=status.HTTP_409_CONFLICT)
            else: 
                return Response({'error':'No puede iniciar sesión'},status=status.HTTP_401_UNAUTHORIZED)
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
                return Response({'Sesión':'Salida completada!'},status=status.HTTP_200_OK)

            return Response({'error':'No existe usuario con estas credenciales'},status=status.HTTP_400_BAD_REQUEST)
        
        except:
            return Response({'error':'No existe este token'},status=status.HTTP_409_CONFLICT) 
        


# Register (Register)
class Register(APIView):
    
    def post(request:str,*args, **kwargs) -> Response:
        user = request.data
        return




# List Items (Dashboard)
class ShowItems():
    pass


# Detail Items (Dashboard)
class DetailItem():
    pass



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
class Profile():
    pass

# Profile Update (Profile)
class ProfileUpdate():
    pass

# Profile Delete (Profile)
class DeleteProfile():
    pass