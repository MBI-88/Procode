from django.db import models
from django.conf import settings
from django.urls import reverse

# Create your models here.

class ProfileUser(models.Model):
    """
    Tabla de Registro de usuarios
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="profile")
    phone = models.CharField(max_length=20)
    created_date = models.DateTimeField(auto_now_add=True,db_index=True)
    image = models.ImageField(upload_to='user/%Y/%m/%d',blank=True)
    address = models.CharField(max_length=100,null=True)

    class Meta:
        ordering = ['-created_date']
    
    def __str__(self) -> str:
        return f'Profile for user {self.user.username}'



class ShopingCell(models.Model):
    """
    Tabla para el guardado de datos de telefonos
    """
    owner_user = models.ForeignKey('auth.User',related_name='shopingcell',on_delete=models.CASCADE)
    model_name = models.CharField(max_length=100,db_index=True)
    slug = models.SlugField(max_length=100,db_index=True,unique=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    image = models.ImageField(upload_to='cells/%Y/%m/%d',blank=True)
    desciption = models.TextField(max_length=1000,blank=True)

    class Meta:
        ordering = ['-updated_date']
        
        
    def __str__(self) -> str:
        return f'Item cell {self.model_name}'
    
    def get_absolute_url(self):
        return reverse("cells:model_detail", args=[self.id,self.slug])
    

