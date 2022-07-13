from rest_framework import generics,viewsets
from ..models import ProfileUserModel,ShopingCellModel
from django.contrib.auth.models import User
from .serializers import ShopingCellModelSerializer,ProfileUserModelSerializer,UserModelSerializer
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger

# Views

# Login (Register)
class Login():
    pass

# Register (Register)
class Register():
    pass


# List Items (Dashboard)
class ShowItems(generics.ListAPIView):
    pagination_class = Paginator
    paginate_by = 15
    queryset = ShopingCellModel.objects.all()
    serializer_class = ShopingCellModelSerializer


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