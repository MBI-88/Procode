from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils.text import slugify

# ****************************************** Profile Model *****************************************************

class ProfileUserModel(models.Model):
    """
    Tabla de Registro de usuarios
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="profile")
    phone = models.CharField(max_length=8)
    created_date = models.DateTimeField(auto_now_add=True,db_index=True)
    updated_date = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='images/user/%Y/%m/%d',blank=True,null=True)
    address = models.CharField(max_length=200,null=True)

    class Meta:
        ordering = ['-created_date']
    
    
    def __str__(self) -> str:
        return f'Profile for user {self.user.username}'

   

# ************************************************* Shoping Model ***************************************************

class ShopCellModel(models.Model):
    """
    Tabla para el guardado de los articulos de venta
    """
    profile = models.ForeignKey(ProfileUserModel,on_delete=models.CASCADE,null=True,related_name='shopcell')
    model_name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=150,blank=True,unique=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True,db_index=True)
    price = models.FloatField(max_length=6)
    image = models.ImageField(upload_to='images/smartphone/%Y/%m/%d',blank=True,null=True)
    description = models.TextField(max_length=1000,null=True)

    class Meta:
        ordering = ['-updated_date']
        
        
    def __str__(self) -> str:
        return f'Item cell {self.model_name}'
    

    def get_absolute_url(self):
        return reverse("cells:dashboar_detail", kwargs={'pk':self.pk})
    

    def save(self,*args, **kwargs) -> None:
        if not self.slug:
            self.slug = slugify(self.model_name +'-'+ str(self.profile.user.username))
        super().save(*args,**kwargs)



