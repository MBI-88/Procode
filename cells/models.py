from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils.text import slugify

# Create your models here.

class ProfileUser(models.Model):
    """
    Tabla de Registro de usuarios
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="profile")
    phone = models.CharField(max_length=20)
    created_date = models.DateTimeField(auto_now_add=True,db_index=True)
    updated_date = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='user/%Y/%m/%d',blank=True)
    address = models.CharField(max_length=100,null=True)

    class Meta:
        ordering = ['-created_date']
    
    def __str__(self) -> str:
        return f'Profile for user {self.user.username}'
    
    def get_absolute_url(self):
        return reverse("cells:update_profile", kwargs={"pk": self.pk})
    
    def get_absolute_url_delete(self):
        return reverse("cells:delete_profile", kwargs={"pk": self.pk})
    
    



class ShopingCell(models.Model):
    """
    Tabla para el guardado de los articulos de venta
    """
    owner_user = models.ForeignKey(settings.AUTH_USER_MODEL,related_name='shopingcell',on_delete=models.CASCADE)
    model_name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100,blank=True,unique=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True,db_index=True)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    image = models.ImageField(upload_to='cells/%Y/%m/%d',blank=True)
    desciption = models.TextField(max_length=1000,blank=True)

    class Meta:
        ordering = ['-updated_date']
        
        
    def __str__(self) -> str:
        return f'Item cell {self.model_name}'
    
    def get_absolute_url(self):
        return reverse("cells:dashboar_detail", kwargs={'pk':self.pk})
    
    def save(self,*args, **kwargs) -> None:
        if not self.slug:
            self.slug = slugify(self.model_name+"-"+self.created_date)
        super().save(*args,**kwargs)

