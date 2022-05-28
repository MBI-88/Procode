from django.db import models
from django.contrib.auth.backends import UserModel

# Create your models here.

class ShopingCell(models.Model):
    model_name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    created_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    price = models.IntegerField()
    image = models.ImageField()

    class Meta:
        pass

