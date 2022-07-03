from django import forms
import re
from cells.models import ShopingCellModel
from django.contrib.auth.models import User

#  Users
class LoginForm(forms.Form):
    username = forms.CharField(max_length=25,required=True)
    password = forms.CharField(widget=forms.PasswordInput,required=True)


class UserRegistrationForm(forms.Form):
    username = forms.CharField(max_length=25,required=True)
    first_name = forms.CharField(max_length=50,required=True)
    last_name = forms.CharField(max_length=100,required=True)
    password = forms.CharField(widget=forms.PasswordInput,required=True)
    password2 = forms.CharField(widget=forms.PasswordInput,required=True)
    email = forms.EmailField()
    phone = forms.CharField(max_length=8,required=True)
    


    def clean_password2(self) -> str:
        cd = self.cleaned_data
        if (cd['password'] != cd['password2']):
            raise forms.ValidationError('Las claves no coinciden')
        
        return cd['password2']
    
    def clean_phone(self) -> str:
        cd = self.cleaned_data
        pattern = re.compile("^5[1-8]")   
        if (len(cd['phone']) == 8):
            if (pattern.search(cd['phone'])):
                return cd['phone']
        raise forms.ValidationError('El numero no coincide con el prefijo del sistema')

    
    
class UpdateUserForm(forms.Form):
    username = forms.CharField(max_length=25,required=True)
    first_name = forms.CharField(max_length=50,required=True)
    last_name = forms.CharField(max_length=100,required=True)
    email = forms.EmailField()
    phone = forms.CharField(max_length=8,required=True)
    image = forms.ImageField()
    address = forms.CharField(max_length=100,required=True)


    def clean_phone(self) -> str:
        cd = self.cleaned_data
        pattern = re.compile("^5[1-8]")   
        if (len(cd['phone']) == 8):
            if (pattern.search(cd['phone'])):
                return cd['phone']
        raise forms.ValidationError('El numero no coincide con el prefijo del sistema')



class DeleteUserForm(forms.Form):
    delete = forms.CharField(widget=forms.CheckboxInput)




# Items
class DeleteItemForm(forms.Form):
    delete = forms.CharField(widget=forms.CheckboxInput)


class UpdateItemForm(forms.ModelForm):
    
    class Meta:
        model = ShopingCellModel
        fields = ['model_name','price','image','description']

    




