from django.shortcuts import redirect, render,get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.utils.decorators import method_decorator
from django.views.generic import ListView,DetailView,View,TemplateView
from django.http import HttpResponse,HttpResponseServerError
from .forms import LoginForm,UserRegistrationForm
from .models import ShopingCell
from django.contrib.auth.views import (LoginView,LogoutView,PasswordResetDoneView,
                                        PasswordResetView,PasswordResetCompleteView,PasswordResetConfirmView)
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib import messages
from .models import ProfileUser
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from threading import Thread



# Send Email
def sendEmail(subject:str,message:dict,recipient_list:str,name_thred:str) -> None:
    thred = Thread(target=send_mail,args=[subject,message,'procodecubashop@gmail.com',
                    [recipient_list]],name=name_thred)
    thred.start()


# Create your views here.

# Index
def index(request:str) -> render:
    """
    Index view 
    methods: request.GET
    """
    return render(request,'cell_index.html')


# Login (Register)
class LoginUser(LoginView):
    """
    LoginUser view
    methods: request.GET, request.POST
    LoginView's son
    """
    template_name = 'accounts/registration/login.html'
    form_class = LoginForm
    
    
  
# Logged out (Register)
class LoggedoutUser(LogoutView):
    """
    LoggedoutUser view
    methods: request.GET
    LogoutView's son
    """
    template_name = 'accounts/registration/logged_out.html'
    title = 'Logged out'


# Register (Register)
class RegisterUser(View):
    """
    RegisterUser view
    methods: request.GET, request.POST
    View's son
    """
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
                    return redirect('index')

                except:
                    return HttpResponseServerError('errors/500.html')
        
            else:
                messages.add_message(request,level=messages.WARNING,message='This user olready exist!')
        
        return render(request,self.template_name,{'form':form})
    


# Registration succefull  (Register)
def registrationUserDone(request:str,uid64:bytes,token:str) -> render:
    """
    registrationUserDone view
    methods: request.GET

    """
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


# Reset Password (Register)
class ResetUserPassword(PasswordResetView):
    """
    ResetUserPassword view
    method: request.GET, request.POST
    PassWordResetView's son
    """
    template_name = 'accounts/registration/reset_password.html'
    email_template_name = 'email/email.html'


# Reset Done (Register)
class ResetUserPasswordDone(PasswordResetDoneView):
    """
    ResetUserPasswordDone view
    methods: request.GET
    PasswordResetDoneView's son
    """
    template_name = 'accounts/registration/reset_password_done.html'


# Reset Confirmation (Register)
class ResetUserPasswordConfirm(PasswordResetConfirmView):
    """
    ResetUserPasswordConfirm view
    methods: request.GET, request.POST
    PasswordResetConfirmView's son
    """
    template_name = 'accounts/registration/reset_password_confirm.html' # lleva formulario


# Reset Complete (Register)
class ResetUserPasswordComplete(PasswordResetCompleteView):
    """
    ResetUserPasswordComplete view
    method: request.GET
    PasswordCompleteView's son
    """
    template_name = 'accounts/registration/reset_password_complete.html'



# List Items (Dashboard)
class ShowItems(ListView):
    """
    ShowItems view
    methods: request.GET, request.AJAX
    ListView's son
    """
    template_name = 'dashboard/cell_items.html'
    model = ShopingCell
    context_object_name = 'itemcells'

    def get(self, request:str, *args, **kwargs) -> render:
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        items = self.model.objects.all()
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
            return render(request,'dashboard/items_ajax.html',{self.context_object_name:items})

        return render(request,self.template_name,{self.context_object_name:items})
    


# Detail Items (Dashboard)
class DetailItem(DetailView):
    """
    DetailItem view
    method: request.GET
    DetailView's son
    """
    template_name = 'dashboard/item_detail.html'
    model = ShopingCell
    context_object_name = 'itemcell'



# Create Item (Profile)
class CreateItem(CreateView):
    """
    CreateItem view
    methods: request.GET, request.POST
    CreateView's son
    """
    template_name = 'accounts/profile/create_item.html'
    model = ShopingCell
    fields = ['model_name','slug','price','image','description']

    @method_decorator(login_required)
    def dispatch(self, request:str, *args, **kwargs) -> HttpResponse:
        return super().dispatch(request, *args, **kwargs)


# Update Item (Profile)
class UpdateItem(UpdateView):
    """
    UpdateItem view
    methods: request.GET, reques.POST
    UpdateView's son
    """
    template_name = 'accounts/profile/update_item.html'
    model = ShopingCell
    fields = ['price','image','description']

    @method_decorator(login_required)
    def dispatch(self, request:str, *args, **kwargs) -> HttpResponse:
        return super().dispatch(request, *args, **kwargs)



# Delete Item (Profile)
class DeleteItem(DeleteView):
    """
    DeletItem view
    methods: request.GET, request.POST
    DeleteView's son
    """
    template_name = 'accounts/profile/delete_item.html'
    model = ShopingCell
    success_url = reverse_lazy('profile')

    @method_decorator(login_required)
    def dispatch(self, request:str, *args, **kwargs) -> HttpResponse:
        return super().dispatch(request, *args, **kwargs)




# Profile (Profile)
class ProfileUser(TemplateView):
    """
    ProfileUser view
    methods: request.GET, request.POST
    TemplateView's son
    """
    template_name = 'accounts/profile/cell_profile.html'

    @method_decorator(login_required)
    def get(self,request:str,*args, **kwargs) -> HttpResponse:
        context = super().get_context_data(**kwargs)
        context["user"] = get_object_or_404(User,username=request.user.username,is_active=True)
        return context



# Profile Update (Profile)
class UpdateProfile(UpdateView):
    """
    UpdateProfile view
    methods: request.GET, request.POST
    UpdateView's son
    """
    template_name = 'accounts/profile/update_profile.html'
    form_class = UserRegistrationForm
    context_object_name = 'form_update'
    

    @method_decorator(login_required)
    def get(self, request:str, *args, **kwargs) -> HttpResponse:
        form = self.form_class(initial={
                'username': request.user.username,
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
                'email': request.user.email,
                'phone': request.user.profile.phone,
                'image': request.user.profile.image,
                'address': request.user.profile.address
        })

        return render(request,self.template_name,{self.context_object_name:form})
    

    @method_decorator(login_required)
    def post(self, request:str, *args, **kwargs) -> HttpResponse:
        form = self.form_class(request.POST)
        cd = form.cleaned_data
        if form.is_valid():
            if form.has_changed():
                new_user = get_object_or_404(User,username=request.user.username,is_active=True)
                new_user.username = cd['username']
                new_user.first_name = cd['first_name']
                new_user.last_name = cd['last_name']
                new_user.email = cd['email']
            
                #email
                subject = 'ProC0d3 Activaion\'account' 
                message = render_to_string('email/email.html',{
                    'domain': get_current_site(request),
                    'user': new_user.username,
                    'body':"Your profile account was updated successful!"
                })
                    
                # email_sender
                try:
                    sendEmail(subject,message,cd['email'],new_user.username)
                    new_user.save()
                    ProfileUser.objects.filter(user=new_user).update(phone=cd['phone'],
                                            image=cd['image'],address=cd['address'])
                    
                    messages.add_message(request,level=messages.SUCCESS,message="Updating successful!")

                    # redireccion
                    return redirect('profile')

                except:
                    return HttpResponseServerError('errors/500.html')
            
            else:
                messages.add_message(request,level=messages.INFO,message="There are not changes in your profile")
                return redirect('profile')
        
        return render(request,self.template_name,{self.context_object_name:form})



# Profile Delete (Profile)
class DeleteProfileUser(DeleteView):
    """
    DeleteProfile view
    methods: request.GET, request.POST
    DeleteView's son
    """
    template_name = 'accounts/profile/delete_account.html'
    model = User
    success_url = reverse_lazy('index')

    @method_decorator(login_required)
    def dispatch(self, request:str, *args, **kwargs) -> HttpResponse:
        return super().dispatch(request, *args, **kwargs)

    
  