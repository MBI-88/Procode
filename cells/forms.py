from email.mime import image
from django import forms


# Forms

class LoginForm(forms.Form):
    username = forms.CharField(max_length=50,attrs={'class':'forms'})
    password = forms.CharField(widget=forms.PasswordInput,attrs={'class':'forms'})


class UserRegistrationForm(forms.Form):
    username = forms.CharField(max_length=25,attrs={'class':'forms'})
    first_name = forms.CharField(max_length=50,attrs={'class':'forms'})
    last_name = forms.CharField(max_length=100,attrs={'class':'forms'})
    password = forms.CharField(widget=forms.PasswordInput,attrs={'class':'forms'})
    password2 = forms.CharField(widget=forms.PasswordInput,attrs={'class':'forms'})
    email = forms.EmailField(attrs={'class':'forms'})
    phone = forms.CharField(max_length=15,attrs={'class':'forms'})
    image = forms.ImageField(attrs={'class':'forms'})
    address = forms.CharField(max_length=100,attrs={'class':'forms'})


    
    def clean_password2(self) -> str:
        cd = self.cleaned_data
        if (cd['password'] != cd['password2']):
            raise forms.ValidationError('Passwords don\'t match')
        
        return cd['password2']



