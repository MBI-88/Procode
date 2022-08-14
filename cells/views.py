from django.shortcuts import redirect,render
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes,force_str
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.utils.decorators import method_decorator
from django.views.generic import View
from django.http import HttpResponse
from .forms import (LoginForm,UserRegistrationForm,DeleteItemForm,UpdateItemForm,DeleteUserForm,UpdateUserForm,ChangePasswordForm,RestorePassowrdForm)
from .models import ShopingCellModel,ProfileUserModel
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from threading import Thread
import re

# ************************************* Email tool ************************************************

# Send Email
def sendEmail(subject:str,message:dict,recipient_list:str,name_thred:str) -> None:
    thred = Thread(target=send_mail,args=[subject,message,'procode@gmail.com',
                    [recipient_list],True],name=name_thred)
    thred.start()

# **************************************** Function Views ************************************************

# Index
def index(request:str) -> HttpResponse:
    """
    Index view 
    methods: request.GET
    """
    return render(request,'cell_index.html')

def contact(request:str) -> HttpResponse:
    """
    Contact view
    methods: request.GET
    """
    return render(request,'dashboard/cell_contact.html')

def info(request:str) -> HttpResponse:
    """
    Info view
    methods: request.GET
    """
    return render(request,'dashboard/cell_info.html')

def who(request:str) -> HttpResponse:
    """
    Who view
    methods: request.GET
    """
    return render(request,'dashboard/cell_who.html')


# ********************************************* Login View ***********************************************

# Login (Register)
class LoginUser(View):
    """
    LoginUser view
    methods: request.GET, request.POST
    View's son
    """
    template_name = 'accounts/registration/login.html'
    form_class = LoginForm
    context_object_name = 'form'
    
    def get(self, request:str, *args, **kwargs) -> HttpResponse:
        form = self.form_class()
        return render(request,self.template_name,{self.context_object_name:form})
    
    def post(self, request:str, *args, **kwargs) -> HttpResponse:
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,username=cd['username'],password=cd['password'])
            if user is not None:
                login(request,user=user)
                return HttpResponse('302')
            messages.add_message(request,level=messages.INFO,message='Usuario no activo o credenciales incorrectas')
        return render(request,self.template_name,{self.context_object_name:form})
    
    
# ******************************************* Register Views **************************************************

# Register (Register)
class Register(View):
    """
    RegisterUser view
    methods: request.GET, request.POST
    View's son
    """
    template_name = 'accounts/registration/register.html'
    form_class = UserRegistrationForm
    context_object_name = 'form'
    model = User

    def get(self,request:str, *args, **kwargs) -> HttpResponse:
        form = self.form_class()
        return render(request,self.template_name,{self.context_object_name:form})

    def post(self,request:str, *args, **kwargs) -> HttpResponse:
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if not self.model.objects.filter(email=cd['email']).exists():
                new_user = self.model()
                new_user.username = cd['username']
                new_user.is_active = False
                new_user.set_password(cd['password'])
                new_user.first_name = cd['first_name']
                new_user.last_name = cd['last_name']
                new_user.email = cd['email']
                # email_sender
                try:
                    new_user.save()
                    ProfileUserModel.objects.create(user=new_user,phone=cd['phone'])
                    #email
                    subject = 'ProC0d3 Registro de usuario' 
                    message = render_to_string('email/email_register.html',{
                        'domain': get_current_site(request),
                        'user': new_user.username,
                        'uid': urlsafe_base64_encode(force_bytes(new_user.pk)),
                        'token': default_token_generator.make_token(new_user),
                        'protocol': request.scheme,
                    })
                    sendEmail(subject,message,cd['email'],new_user.username)
                    messages.add_message(request,level=messages.SUCCESS,message='Registro completado.Siga el enlace enviado a su e-mail')  
                    # redireccion
                    return HttpResponse('302')
                except:
                    messages.add_message(request,level=messages.WARNING,message='El nombre de usuario ya existe') 
            else:
                messages.add_message(request,level=messages.WARNING,message='El e-mail ya existe en nuestro sistema')
        return render(request,self.template_name,{self.context_object_name:form})
    


# Registration succefull  (Register) Pendiente
def registrationUserDone(request:str,uidb64:bytes,token:str) -> HttpResponse:
    """
    registrationUserDone view
    methods: request.GET
    """
    try:
        pk = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=pk)
    except(TypeError,ValueError,OverflowError,User.DoesNotExist):
        user = None

    if (user is not None and default_token_generator.check_token(user,token)):
        user.is_active = True
        user.save()
    else:
        return render(request,'dashboard/token_fail.html')
    messages.add_message(request,level=messages.SUCCESS,message='Ya puede entrar a su cuenta')
    return redirect('cells:index') 


# **************************************** Dashboard Views **********************************************

# List Items (Dashboard)
class ShowItems(View):
    """
    ShowItems view
    methods: request.GET, request.AJAX
    View's son
    """
    template_name = 'dashboard/cell_items.html'
    model = ShopingCellModel
    context_object_name = 'itemcells'

    def get(self, request:str, *args, **kwargs) -> HttpResponse:
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        search = request.GET.get('search')
        page = request.GET.get('page')

        #Sanetizando la busqueda
        pattern = re.compile("[a-zA-Z0-9\s]+")
        if search is not None and pattern.search(search):
            items =  self.model.objects.filter(model_name__icontains=search) 
        else: items = self.model.objects.all()
        paginator = Paginator(items,15)

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
class DetailItem(View): 
    """
    DetailItem view
    method: request.GET
    View's son
    """
    template_name = 'dashboard/item_detail.html'
    model = ShopingCellModel
    context_object_name = 'itemcell'

    def get(self,request:str,*args, **kwargs) -> HttpResponse:
        pk = kwargs['pk']
        item = self.model.objects.get(pk=pk)
        return render(request,self.template_name,{self.context_object_name:item})


# ********************************************* Profile Views ****************************************************

# Create Item (Profile)
class CreateItem(View):
    """
    CreateItem view
    methods: request.GET, request.POST
    View's son
    """
    template_name = 'accounts/profile/create_item.html'
    model = ShopingCellModel
    form_class = UpdateItemForm
    context_object_name = 'form'

    @method_decorator(login_required)
    def get(self,request:str,*args, **kwargs) -> HttpResponse:
        form = self.form_class()
        return render(request,self.template_name,{self.context_object_name:form})
    
    @method_decorator(login_required)
    def post(self,request:str,*args, **kwargs) -> HttpResponse:
        form = self.form_class(request.POST,files=request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            self.model.objects.create(owner_user=request.user,profile=request.user.profile,
            model_name=cd['model_name'],price=cd['price'],
            image=cd['image'],description=cd['description']
            )
            messages.add_message(request,level=messages.SUCCESS,message='Articulo creado con exito')
            return redirect('cells:profile')
        messages.add_message(request,level=messages.WARNING,message='Errores en la creación del articulo')
        return render(request,self.template_name,{self.context_object_name:form})



# Update Item (Profile)
class UpdateItem(View):
    """
    UpdateItem view
    methods: request.GET, reques.POST
    View's son
    """
    template_name = 'accounts/profile/update_item.html'
    model = ShopingCellModel
    form_class = UpdateItemForm
    context_object_name = 'form'

    @method_decorator(login_required)
    def get(self, request:str, *args, **kwargs) -> HttpResponse:
        item = self.model.objects.get(pk=kwargs['pk'])
        form = self.form_class(initial={
            'model_name':item.model_name,
            'image':item.image,
            'price':item.price,
            'description':item.description,
        })
        return render(request,self.template_name,{self.context_object_name:form})
    

    @method_decorator(login_required)
    def post(self, request:str, *args, **kwargs) -> HttpResponse:
        user_item = self.model.objects.get(pk=kwargs['pk'])
        if request.user.username == user_item.owner_user.username:
            form = self.form_class(request.POST,files=request.FILES,instance=user_item)
            if form.is_valid():
                if form.has_changed():
                    form.save()
                    messages.add_message(request,level=messages.SUCCESS,message='Articulo actualizado con exito')
                return redirect('cells:profile')
            messages.add_message(request,level=messages.WARNING,message='Errores en la modificación del articulo')
        else:
            messages.add_message(request,level=messages.WARNING,message='Este no tu articulo')
        return render(request,self.template_name,{self.context_object_name:self.form_class})
        

# Delete Item (Profile)
class DeleteItem(View):  
    """
    DeletItem view
    methods: request.GET, request.POST
    View's son
    """
    template_name = 'accounts/profile/delete_item.html'
    model = ShopingCellModel
    form_class = DeleteItemForm
    context_object_name = 'form'
    
    @method_decorator(login_required)
    def get(self, request:str, *args, **kwargs) -> HttpResponse:
        form = self.form_class()
        return render(request,self.template_name,{self.context_object_name:form,'pk':kwargs['pk']})

    @method_decorator(login_required)
    def post(self, request:str, *args, **kwargs) -> HttpResponse:
        form = self.form_class(request.POST)
        user_item = self.model.objects.get(pk=kwargs['pk'])
        if request.user.username == user_item.owner_user.username:
            if form.is_valid():
                self.model.objects.filter(pk=kwargs['pk']).delete()
                messages.add_message(request,level=messages.SUCCESS,message='Articulo eliminado con exito')
        else:
            messages.add_message(request,level=messages.WARNING,message='Este no tu articulo')
        return redirect('cells:profile')

    

# Profile (Profile)
class Profile(View):
    """
    ProfileUser view
    methods: request.GET, request.POST
    View's son
    """
    template_name = 'accounts/profile/cell_profile.html'
    model = ShopingCellModel
    context_object_name = 'items'

    @method_decorator(login_required)
    def get(self,request:str,*args, **kwargs) -> HttpResponse:
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        search = request.GET.get('search')
        page = request.GET.get('page')

        # Sanetizando busqueda
        pattern = re.compile("[a-zA-Z0-9\s]+")

        if search is not None and pattern.search(search):
            items = self.model.objects.filter(owner_user=request.user).filter(model_name__icontains=search)
        else: items = self.model.objects.filter(owner_user=request.user)
        
        paginator = Paginator(items,15)

        try:
            items = paginator.page(page)
        except PageNotAnInteger:
            items = paginator.page(1)
        except EmptyPage:
            if is_ajax:
                return HttpResponse('')
            items = paginator.page(paginator.num_pages)
        
        if is_ajax:
            return render(request,'accounts/profile/user_items_list.html',{self.context_object_name:items})
        return render(request,self.template_name,{self.context_object_name:items})



# Profile Update (Profile)
class UpdateProfile(View):
    """
    UpdateProfile view
    methods: request.GET, request.POST
    View's son
    """
    template_name = 'accounts/profile/update_profile.html'
    form_class = UpdateUserForm
    model = User
    context_object_name = 'form'
    
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
        request.user.email = ''
        request.user.save()
        return render(request,self.template_name,{self.context_object_name:form})
    
    @method_decorator(login_required)
    def post(self, request:str, *args, **kwargs) -> HttpResponse:
        form = self.form_class(request.POST,files=request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            if not self.model.objects.filter(email=cd['email']).exists():
                request.user.username = cd['username']
                request.user.first_name = cd['first_name']
                request.user.last_name = cd['last_name']
                request.user.email = cd['email']
                request.user.is_active = False
                request.user.profile.phone = cd['phone']
                request.user.profile.address = cd['address']
                request.user.profile.image = cd['image']   
                # email_sender
                try:
                    request.user.save()
                    request.user.profile.save()
                    #email
                    subject = 'ProC0d3 Actualización de perfil de usuario' 
                    message = render_to_string('email/email_profile.html',{
                        'domain': get_current_site(request),
                        'user': request.user.username,
                        'uid': urlsafe_base64_encode(force_bytes(request.user.pk)),
                        'token': default_token_generator.make_token(request.user),
                        'protocol': request.scheme,
                    })
                    sendEmail(subject,message,cd['email'],cd['username'])
                    messages.add_message(request,level=messages.SUCCESS,message="Perfil actualizado siga el link en su e-mail")
                    # redireccion
                    return redirect('cells:logout')
                except:
                    messages.add_message(request,level=messages.WARNING,message='El nombre de usuario ya existe') 
            else:
                messages.add_message(request,level=messages.WARNING,message='El e-mail ya existe en nuestro sistema')
        return render(request,self.template_name,{self.context_object_name:form})



# Profile Delete (Profile)
class DeleteProfile(View):
    """
    DeleteProfile view
    methods: request.GET, request.POST
    View's son
    """
    template_name = 'accounts/profile/delete_account.html'
    model = User
    form_class = DeleteUserForm
    context_object_name = 'form'
    
    @method_decorator(login_required)
    def get(self,request:str, *args, **kwargs) -> HttpResponse:
        form = self.form_class()
        return render(request,self.template_name,{self.context_object_name:form})
    
    @method_decorator(login_required)
    def post(self,request:str,*args, **kwargs) -> HttpResponse:
        form = self.form_class(request.POST)
        if form.is_valid():
            self.model.objects.filter(username=request.user.username).delete()
            messages.add_message(request,level=messages.SUCCESS,message='Su cuenta fue eliminada')
            return HttpResponse('302')
        


# Profile Canche password (Profile)
class ChangePasswordProfile(View):
    form_class = ChangePasswordForm
    context_object_name = 'form'
    template_name = 'accounts/registration/change_password.html'

    @method_decorator(login_required)
    def get(self,request:str, *args, **kwargs) -> HttpResponse:
        form = self.form_class()
        return render(request,self.template_name,{self.context_object_name:form})
    
    @method_decorator(login_required)
    def post(self,request:str,*args, **kwargs) -> HttpResponse:
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if authenticate(request,username=request.user.username,password=cd['currentpassword']) is not None:
                request.user.set_password(cd['newpassword'])
                request.user.is_active = False
                request.user.save()
                    #email
                subject = 'ProC0d3 Cambio de password de usuario' 
                message = render_to_string('email/email_password.html',{
                    'domain': get_current_site(request),
                    'user': request.user.username,
                    'uid': urlsafe_base64_encode(force_bytes(request.user.pk)),
                    'token': default_token_generator.make_token(request.user),
                    'protocol': request.scheme,
                })
                sendEmail(subject,message,request.user.email,request.user.username)
                messages.add_message(request,level=messages.SUCCESS,message='Siga el enlace que se envio a su e-mail')
                return HttpResponse('302')
            else:
                messages.add_message(request,level=messages.WARNING,message='La clave actual no es válida')
        return render(request,self.template_name,{self.context_object_name:form})


# Restore Password (Profile)
class RestorePassword(View):
    form_class = RestorePassowrdForm
    template_name = 'accounts/registration/restore_password.html'
    context_object_name = 'form'
    model = User

    def get(self,request:str,*args, **kwargs) -> HttpResponse:
        form = self.form_class()
        return render(request,self.template_name,{self.context_object_name:form})
    
    def post(self,request:str,*args, **kwargs) -> HttpResponse:
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            try:
                user = self.model.objects.get(email=cd['email'])
                user.is_active = False
                user.set_password('password1') # hacerlo mas fuerte
                user.save()
                #email
                subject = 'ProC0d3 Restablecimiento de credenciales' 
                message = render_to_string('email/email_restored.html',{
                    'domain': get_current_site(request),
                    'user': user.username,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': default_token_generator.make_token(user),
                    'protocol': request.scheme,
                    'password': 'password1',
                })
                sendEmail(subject,message,cd['email'],user.username)
                messages.add_message(request,level=messages.SUCCESS,message='Siga el enlace que se envio a su e-mail')
                return HttpResponse('302')
            except:
                messages.add_message(request,level=messages.WARNING,message='El e-mail no es válido en nuestro sistema')
        return render(request,self.template_name,{self.context_object_name:form})

