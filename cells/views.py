from django.shortcuts import redirect,render
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,authenticate,logout
from django.contrib.sites.shortcuts import get_current_site
from django.utils.decorators import method_decorator
from django.views.generic import View
from django.http import HttpResponse,HttpResponseServerError
from .forms import (LoginForm,UserRegistrationForm,DeleteItemForm,UpdateItemForm,DeleteUserForm,UpdateUserForm)
from .models import ShopingCellModel,ProfileUserModel
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from threading import Thread



# Send Email
def sendEmail(subject:str,message:dict,recipient_list:str,name_thred:str) -> None:
    thred = Thread(target=send_mail,args=[subject,message,'procodecubashop@gmail.com',
                    [recipient_list]],name=name_thred)
    thred.start()


# Create your views here.

# Index
def index(request:str) -> HttpResponse:
    """
    Index view 
    methods: request.GET
    """
    return render(request,'cell_index.html')


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
                if (user.is_active):
                    login(request,user=user)
                    return HttpResponse('302')
                else:
                    messages.add_message(request,level=messages.WARNING,message='El usuario no esta activo')
                    return render(request,self.template_name,{self.context_object_name:form})


        return render(request,self.template_name,{self.context_object_name:form})
    
    

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
            new_user = self.model()
            new_user.username = cd['username']
            new_user.is_active = True
            new_user.set_password(cd['password'])
            new_user.first_name = cd['first_name']
            new_user.last_name = cd['last_name']
            new_user.email = cd['email']

            #email
            subject = 'ProC0d3 Activaion\'account' 
            message = render_to_string('email/email_register.html',{
                'domain': get_current_site(request),
                'user': new_user.username,
                'uid': urlsafe_base64_encode(force_bytes(new_user.pk)),
                'token': default_token_generator.make_token(new_user),
                'protocol': request.scheme,
            })
                
            # email_sender
            try:
                sendEmail(subject,message,cd['email'],new_user.username)
                new_user.save()
                ProfileUserModel.objects.create(user=new_user,phone=cd['phone'])
                    
                # redireccion
                return HttpResponse('302')
            except:
                return HttpResponseServerError('errors/500.html')
        else:
            messages.add_message(request,level=messages.WARNING,message='Este nombre de usuario ya existe')
        return render(request,self.template_name,{self.context_object_name:form})
    


# Registration succefull  (Register)
def registrationUserDone(request:str,uid64:bytes,token:str) -> HttpResponse:
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
        return render(request,'') # El token no es valido/ pendiente (404)
    return redirect('cells:index') # Respuesta correcta y redirección


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
    
        if search is not None:
            # Sanetizar search
            items = self.model.objects.filter(model_name__icontains=search)
        else:
            items = self.model.objects.all()

        count = len(items)
        orphans = count - 8 if count > 8 else 0
        paginator = Paginator(items,8,orphans=orphans)

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
        pk = request.GET.get('pk')
        item = self.model.objects.get(pk=pk)
        return render(request,self.template_name,{self.context_object_name:item})



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
            return redirect('cells:profile')
        messages.add_message(request,level=messages.WARNING,message='Errores en la creacion del articulo')
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
        item = self.model.objects.get(pk=request.GET.get('pk'))
        form = self.form_class(initial={
            'model_name':item.model_name,
            'image':item.image,
            'price':item.price,
            'description':item.description,
        })
        return render(request,self.template_name,{self.context_object_name:form})
    

    @method_decorator(login_required)
    def post(self, request:str, *args, **kwargs) -> HttpResponse:
        item = self.model.objects.get(pk=request.POST.get('pk'))
        form = self.form_class(request.POST,instance=item)
        if form.is_valid():
            if form.has_changed():
                form.save()
            return redirect('cells:profile')
        messages.add_message(request,level=messages.WARNING,message='Errores en la modificación del articulo')
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
        pk = request.GET.get('pk')
        return render(request,self.template_name,{self.context_object_name:form,'pk':pk})
    

    @method_decorator(login_required)
    def post(self, request:str, *args, **kwargs) -> HttpResponse:
        form = self.form_class(request.POST)
        if form.is_valid():
            self.model.objects.filter(pk=request.POST.get('pk')).delete()
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
    
        if search is not None:
            # Sanetizar search
            items = self.model.objects.filter(owner_user=request.user).filter(model_name__icontains=search)
        else:
            items = self.model.objects.filter(owner_user=request.user)
        
        count = len(items)
        orphans = count - 8 if count > 8 else 0
        paginator = Paginator(items,8,orphans=orphans)

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
        return render(request,self.template_name,{self.context_object_name:form})
    

    @method_decorator(login_required)
    def post(self, request:str, *args, **kwargs) -> HttpResponse:
        form = self.form_class(request.POST,files=request.FILES)
        if form.is_valid():
            if form.has_changed():
                cd = form.cleaned_data
                request.user.username = cd['username']
                request.user.first_name = cd['first_name']
                request.user.last_name = cd['last_name']
                request.user.email = cd['email']
                request.user.save()
                
                request.user.profile.phone = cd['phone']
                request.user.profile.address = cd['address']
                request.user.profile.image = cd['image']
                request.user.profile.save()
                
                

                #email
                subject = 'ProC0d3 Activaion\'account' 
                message = render_to_string('email/email_profile.html',{
                    'domain': get_current_site(request),
                    'user': cd['username'],
                    'body':"Su perfil se actualizó con exito!"
                })
                        
                # email_sender
                try:
                    sendEmail(subject,message,cd['email'],cd['username'])
                    messages.add_message(request,level=messages.SUCCESS,message="Perfil actualizado!")

                    # redireccion
                    return redirect('cells:profile')
                except:
                    return HttpResponseServerError('errors/500.html') 
                
            else:
                messages.add_message(request,level=messages.INFO,message="No se realizaron cambios")
                return redirect('cells:profile')
       
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
            logout(request)
            return redirect('cells:index')
        




