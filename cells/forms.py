from django import forms
from django.contrib.auth.models import User 
from .models import ProfileUser

# Forms

class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput)

class UserRegistration(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput,label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput,label='Confirm')

    class Meta:
        model = User
        fields = ('username','first_name','email')
    
    def clean_password2(self) -> str:
        cd = self.cleaned_data
        if (cd['password'] != cd['password2']):
            raise forms.ValidationError('Passwords don\'t match')
        
        return cd['password2']

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = ProfileUser
        fields = ('image','address','phone')