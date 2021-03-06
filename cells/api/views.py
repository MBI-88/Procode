from rest_framework.views import APIView
from rest_framework.generics import ListAPIView,RetrieveAPIView
from rest_framework.viewsets import ModelViewSet
from ..models import ShopingCellModel
from .serializers import ShopingCellModelSerializer,UserRegistrationSerializer,UpdateUserSerializer,UserSerializer 
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework import status
from rest_framework.authtoken.models import Token
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
        data = UserRegistrationSerializer(request.data)
        if data.is_valid():
            try:
                data.save()
                return Response(data={'message':'Usuario registrado!'},status=status.HTTP_201_CREATED)
            except:
                return Response(data={'message':'Error interno'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(data=data.error_messages,status=status.HTTP_406_NOT_ACCEPTABLE)




# List Items (Dashboard)
class ShowItems(ListAPIView):
    queryset = ShopingCellModel.objects.all()
    serializer_class = ShopingCellModelSerializer
    



# Detail Items (Dashboard)
class DetailItem(RetrieveAPIView):
    queryset = ShopingCellModel.objects.all()
    serializer_class = ShopingCellModelSerializer



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