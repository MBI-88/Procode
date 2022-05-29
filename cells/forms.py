from django import forms
from django.contrib.auth.models import User 
from .models import ProfileUser

# Forms

class LoginForm(forms.Form):
    username = forms.CharField(max_length=50,attrs={'class':'form'})
    password = forms.CharField(widget=forms.PasswordInput,attrs={'class':'form'})


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput,attrs={'class':'form'})
    password2 = forms.CharField(widget=forms.PasswordInput,attrs={'class':'form'})

    def __init__(self,*args, **kwargs) -> None:
        self.fields['username'].widget_attrs({'class':'form'})
        self.fields['first_name'].widget_attrs({'class':'form'})
        self.fields['email'].widget_attrs({'class':'form'})

    class Meta:
        model = User
        fields = ('username','first_name','email')
    
    def clean_password2(self) -> str:
        cd = self.cleaned_data
        if (cd['password'] != cd['password2']):
            raise forms.ValidationError('Passwords don\'t match')
        
        return cd['password2']

class ProfileEditForm(forms.ModelForm):
    def __init__(self,*args, **kwargs) -> None:
        self.fields['image'].widget_attrs({'class':'form'})
        self.fields['address'].widget_attrs({'class':'form'})
        self.fields['phone'].widget_attrs({'class':'form'})

    class Meta:
        model = ProfileUser
        fields = ('image','address','phone')

class UserEditForm(forms.ModelForm):
    def __init__(self,*args, **kwargs) -> None:
        self.fields['username'].widget_attrs({'class':'form'})
        self.fields['first_name'].widget_attrs({'class':'form'})
        self.fields['email'].widget_attrs({'class':'form'})

    class Meta:
        model = User
        fields = ('username','email') 