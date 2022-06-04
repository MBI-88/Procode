from django.shortcuts import redirect, render
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils import timezone
from django.views.generic import ListView,DetailView,View
from django.http import HttpResponse, HttpResponseServerError, JsonResponse
from .forms import LoginForm,UserRegistrationForm
from django.contrib.auth.views import LoginView,LogoutView
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.contrib.auth.models import User
from .models import ProfileUser
import hashlib
from threading import Thread


# Send Email
def sendEmail(recipient_list:str,html_message:str,name_thred:str) -> None:
    thred = Thread(target=send_mail,kwargs={
                    'subject': 'Authenticated\'count',
                    'message':'<h2> Please click here to authenticate <a>...</a></h2>',
                    'from_email':'procodecubashop@gmail.com',
                    'recipient_list':[recipient_list],
                    'html_message': html_message
                    },name=name_thred)
    thred.start()


# Create your views here.

# Route Index
def index(request:str) -> render:
    return render(request,'base.html')


# Route Login
class LoginUser(LoginView):
    template_name = 'accounts/registration/login.html'
    form_class = LoginForm
    next_page = 'accounts/profile/profile.html'
    
  
 

# Route Logged out
class LoggedoutUser(LogoutView):
    template_name = 'accounts/registration/logged_out.html'
    next_page = ''
    title = 'Logged out'


# Route Register
class RgisterUser(View):
    template_name = 'accounts/registration/register.html'
    form_class = UserRegistrationForm
    initial = {
        'username':'Name of the user in the system',
        'first_name': 'Name of the real user',
        'last_name': 'Last name of real user',
        'password': 'Password',
        'password2': 'Confirm',
        'email': 'Email',
        'phone':'Phone',
        'image': 'User\'picture',
        'address': 'Address'
    }

    def get(self,request:str, *args, **kwargs) -> render:
        form = self.form_class(initial=self.initial)
        return render(request,self.template_name,{'form':form})

    
    def post(self,request:str, *args, **kwargs) -> render:
        form = self.form_class(request.POST)
        cd = form.cleaned_data
        if form.is_valid():
            user = User.objects.filter(first_name=cd['first_name'],last_name=cd['last_name'],email=cd['email'])
            if (user is None):
                new_user = User()
                new_user.username = cd['username']
                new_user.is_active = False
                new_user.set_password(cd['password'])
                new_user.first_name = cd['first_name']
                new_user.last_name = cd['last_name']
                new_user.email = cd['email']

                hash = hashlib.md5()
                hash.update(bytes(new_user.username,encoding="utf-8"))
                key_token = hash.hexdigest()
                key_datetoken = timezone.now() + timezone.timedelta(1)

                new_user2 = ProfileUser(phone=cd['phone'],
                                        image=cd['image'],
                                        address=cd['address'],
                                        key_token=key_token,
                                        key_date=key_datetoken)
                
                # email_sender
                try:
                    sendEmail(new_user.email,'Hacer html',new_user.username)
                    new_user.save()
                    new_user2.save()
                    
                    # redireccion

                except:
                    raise HttpResponseServerError('Error to send messages')
                
                

            else:
                return HttpResponse('The user {} is in the system'.format(cd['username']))
        
        return render(request,self.template_name,{'form':form.errors})




# Route List Items
class ShowItems(ListView):
    pass


# Route Detail Items
class DetailItem(DetailView):
    pass