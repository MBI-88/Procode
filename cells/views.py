from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.utils.decorators import method_decorator
from django.views.generic import ListView,DetailView,View
from django.http import HttpResponse, JsonResponse
from .forms import LoginForm,UserRegistrationForm
from .models import ShopingCell
from django.contrib.auth.views import (LoginView,LogoutView,PasswordResetDoneView,
                                        PasswordResetView,PasswordResetCompleteView,PasswordResetConfirmView)
from django.contrib.auth import authenticate
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.contrib.auth.models import User
from .models import ProfileUser
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from threading import Thread



# Send Email
def sendEmail(subject:str,message:dict,recipient_list:str,name_thred:str) -> None:
    thred = Thread(target=send_mail,args=[subject,message,'procodecubashop@gmail.com',
                    [recipient_list]],name=name_thred)
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
            user = User.objects.filter(username=cd['username'])
            if (user is None):
                new_user = User()
                new_user.username = cd['username']
                new_user.is_active = False
                new_user.set_password(cd['password'])
                new_user.first_name = cd['first_name']
                new_user.last_name = cd['last_name']
                new_user.email = cd['email']


                #email
                subject = 'ProC0d3 Activaion\'account' 
                message = render_to_string('email/email.html',{
                    'domain': get_current_site(request),
                    'user': new_user.username,
                    'uid64': urlsafe_base64_encode(force_bytes(new_user.pk)),
                    'token': default_token_generator.make_token(new_user)
                })
                
                # email_sender
                try:
                    sendEmail(subject,message,cd['email'],new_user.username)
                    new_user.save()
                    ProfileUser.objects.create(user=new_user,phone=cd['phone'],
                                        image=cd['image'],
                                        address=cd['address'])
                    
                    # redireccion
                    return redirect('login')

                except:
                    raise render(request,'')
        
            else:
                return render(request,'') 
        
        return render(request,self.template_name,{'form':form})


# Registration succefull
def registrationUserDone(request:str,uid64:bytes,token:str) -> render:
    try:
        uid = urlsafe_base64_decode(uid64).decode()
        user = User.objects.get(pk=uid)
    except(TypeError,ValueError,OverflowError,User.DoesNotExist):
        user = None

    if (user is not None and default_token_generator.check_token(user,token)):
        user.is_active = True
        user.save()
    else:
        user.delete()
        return render(request,'') # El token no es valido

    return redirect('index') # Respuesta correcta y redirección


# Reset Password
class ResetUserPassword(PasswordResetView):
    template_name = 'accounts/registeration/reset_password.html'
    email_template_name = 'email/email.html'


# Reset Done
class ResetUserPasswordDone(PasswordResetDoneView):
    template_name = 'accounts/registration/reset_password_done.html'


# Reset Confirmation
class ResetUserPasswordConfirm(PasswordResetConfirmView):
    template_name = 'accounts/registration/reset_password_confirm.html'


# Reset Complete
class ResetUserPasswordComplete(PasswordResetCompleteView):
    template_name = 'accounts/registration/reset_password_complete.html'



# List Items
class ShowItems(ListView):
    template_name = 'dashboard/cell_items.html'
    model = ShopingCell
    context_object_name = 'itemcells'

    def get(self, request:str, *args, **kwargs) -> render:
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        items = self.model.object.all()
        count = len(items)
        orphans = count - 8 if count > 8 else 0
        paginator = Paginator(items,8,orphans=orphans)
        page = request.GET.get('page')

        try:
            items = paginator.page(page)
        except PageNotAnInteger:
            items = paginator.page(1)
        except EmptyPage:
            if is_ajax:
                return HttpResponse('')
            items = paginator.page(paginator.num_pages)
        
        if is_ajax:
            return render(request,'dashboard/cell_ajax.html',{self.context_object_name:items})

        return render(request,self.template_name,{self.context_object_name:items})
    


# Detail Items
class DetailItem(DetailView):
    template_name = 'dashboard/cell_detail.html'
    model = ShopingCell
    context_object_name = 'itemcell'