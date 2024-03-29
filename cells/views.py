from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.utils.decorators import method_decorator
from django.views.generic import View
from django.contrib.sessions.models import Session
from django.http import HttpResponse
from .forms import (LoginForm, UserRegistrationForm, DeleteItemForm, UpdateItemForm,
                    DeleteUserForm, UpdateUserForm, ChangePasswordForm, RestorePassowrdForm)
from .models import ShopCellModel, ProfileUserModel
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from threading import Thread
import re
import datetime

# ************************************* Email tool ************************************************

# Send Email


def sendEmail(subject: str, message: dict, recipient_list: str, name_thred: str) -> None:
    """Send email, send an email to user en case of changes in your account

    Args:
        subject (str): subject
        message (dict): message
        recipient_list (str): recipient
        name_thred (str): name of the thred (It uses username)
    """

    thred = Thread(target=send_mail, args=[
        subject, message, 'procode@example.com', [recipient_list], True], name=name_thred)
    thred.start()


# **************************************** Function Views ************************************************

def index(request: str) -> HttpResponse:
    """
    Index (home) presentation page
       

    Args:
        request (str): HTTP request

    Returns:
        Object: HTTP response
    """
    return render(request, 'cell_index.html')


def page_400_bad_request(request: str, exception: object, template_name='errors/400.html') -> HttpResponse:
    return render(request, template_name)


def page_403_not_acces(request: str, exception: object, template_name='errors/403.html') -> HttpResponse:
    return render(request, template_name)


def page_404_not_found(request: str, exception: object, template_name='errors/404.html') -> HttpResponse:
    return render(request, template_name)


def page_500_error(request: str, template_name='errors/500.html') -> HttpResponse:
    return render(request, template_name)

# ********************************************* Login View ***********************************************

# Login (Register)


class LoginUser(View):
    """
    Login view, view for login user

    Args:
        View (object): View class

    Returns:
        Object: HTTP response
    """
    template_name = 'accounts/registration/login.html'
    form_class = LoginForm
    context_object_name = 'form'
    queryset = Session.objects.all()

    def get(self, request: str, *args, **kwargs) -> HttpResponse:
        form = self.form_class()
        return render(request, self.template_name, {self.context_object_name: form})

    def post(self, request: str, *args, **kwargs) -> HttpResponse:
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                request, username=cd['username'], password=cd['password'])
            if user is not None:
                all_sessions = self.queryset.filter(expire_date__gte = datetime.datetime.now())
                for session in all_sessions:
                    session_id = session.get_decoded()
                    if user.id == int(session_id.get('_auth_user_id')):
                        session.delete()
                        messages.add_message(request, level=messages.WARNING,
                                             message='Se intentó una doble sesión')
                        return render(request, self.template_name, {self.context_object_name: form})
                login(request, user=user)
                return HttpResponse('302')
            messages.add_message(request, level=messages.INFO,
                                 message='Usuario no activo o credenciales incorrectas')
        return render(request, self.template_name, {self.context_object_name: form})


# ******************************************* Register Views **************************************************

# Register (Register)
class Register(View):
    """
    Register view, view for registering user

    Args:
        View (object): View class

    Returns:
        Object: HTTP response
    """
    template_name = 'accounts/registration/register.html'
    form_class = UserRegistrationForm
    context_object_name = 'form'
    model = User

    def get(self, request: str, *args, **kwargs) -> HttpResponse:
        form = self.form_class()
        return render(request, self.template_name, {self.context_object_name: form})

    def post(self, request: str, *args, **kwargs) -> HttpResponse:
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if not self.model.objects.filter(email=cd['email']).exists():
                new_user = self.model()
                new_user.username = cd['username']
                new_user.set_password(cd['password'])
                new_user.first_name = cd['first_name']
                #new_user.is_active = False
                new_user.last_name = cd['last_name']
                new_user.email = cd['email']
                # email_sender
                try:
                    new_user.save()
                    ProfileUserModel.objects.create(
                        user=new_user, phone=cd['phone'])
                    # email
                    subject = 'ProC0d3 Registro de usuario'
                    message = render_to_string('email/email_register.html', {
                        'domain': get_current_site(request),
                        'user': new_user.username,
                        'uid': urlsafe_base64_encode(force_bytes(new_user.pk)),
                        'token': default_token_generator.make_token(new_user),
                        'protocol': request.scheme,
                    })
                    #sendEmail(subject, message, cd['email'], new_user.username)
                    messages.add_message(
                        request, level=messages.SUCCESS, message='Registro completado.')
                    # redireccion
                    return HttpResponse('302')
                except:
                    messages.add_message(
                        request, level=messages.WARNING, message='El nombre de usuario ya existe')
            else:
                messages.add_message(
                    request, level=messages.WARNING, message='El e-mail ya existe en nuestro sistema')
        return render(request, self.template_name, {self.context_object_name: form})


# Registration succefull  (Register)
def tokenLinkRecived(request: str, uidb64: bytes, token: str) -> HttpResponse:
    """
    Token link recived, function for reciving token

    Args:
        request (str): HTTP request
        uidb64 (bytes): urls base 64 encoder
        token (str): _description_

    Returns:
        Objecte: HTTP response
    """
    try:
        pk = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=pk)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if (user is not None and default_token_generator.check_token(user, token)):
        user.is_active = True
        user.save()
    else:
        return render(request, 'dashboard/token_fail.html')
    messages.add_message(request, level=messages.SUCCESS,
                         message='Ya puede entrar a su cuenta')
    return redirect('cells:index')


# **************************************** Dashboard Views **********************************************

# List Items (Dashboard)
class ShowItems(View):
    """Show items, view for showing items

    Args:
        View (object): View class

    Returns:
        Object: HTTP response
    """
    template_name = 'dashboard/cell_items.html'
    model = ShopCellModel
    context_object_name = 'itemcells'

    def get(self, request: str, *args, **kwargs) -> HttpResponse:
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        search = request.GET.get('search')
        page = request.GET.get('page')
        # Sanetizando la busqueda
        pattern = re.compile("[a-zA-Z0-9\s]+")
        if search is not None and pattern.search(search):
            items = self.model.objects.defer(
                'created_date', 'description', 'slug').filter(model_name__icontains=search)
        else:
            items = self.model.objects.defer(
                'created_date', 'description', 'slug').all()
        paginator = Paginator(items, 15)
        try:
            items = paginator.page(page)
        except PageNotAnInteger:
            items = paginator.page(1)
        except EmptyPage:
            if is_ajax:
                return HttpResponse('')
            items = paginator.page(paginator.num_pages)
        if is_ajax:
            return render(request, 'dashboard/items_ajax.html', {self.context_object_name: items})
        return render(request, self.template_name, {self.context_object_name: items})


# Detail Items (Dashboard)
class DetailItem(View):
    """
    Detail item, view for showing detail items

    Args:
        View (object): View class

    Returns:
        Object: HTTP response
    """
    template_name = 'dashboard/item_detail.html'
    model = ShopCellModel
    context_object_name = 'itemcell'

    def get(self, request: str, *args, **kwargs) -> HttpResponse:
        pk = kwargs['pk']
        item = self.model.objects.select_related(
            'profile__user').defer('created_date', 'slug').get(pk=pk)
        return render(request, self.template_name, {self.context_object_name: item})


# ********************************************* Profile Views ****************************************************

# Create Item (Profile)
class CreateItem(View):
    """
    Create item, view for creating items

    Args:
        View (object): View class

    Returns:
        Object: HTTP response
    """
    template_name = 'accounts/profile/create_item.html'
    model = ShopCellModel
    form_class = UpdateItemForm
    context_object_name = 'form'

    @method_decorator(login_required)
    def get(self, request: str, *args, **kwargs) -> HttpResponse:
        form = self.form_class()
        return render(request, self.template_name, {self.context_object_name: form})

    @method_decorator(login_required)
    def post(self, request: str, *args, **kwargs) -> HttpResponse:
        form = self.form_class(request.POST, files=request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            self.model.objects.create(profile=request.user.profile,
                                      model_name=cd['model_name'], price=cd['price'],
                                      image=cd['image'], description=cd['description']
                                      )
            messages.add_message(
                request, level=messages.SUCCESS, message='Articulo creado con exito')
            return redirect('cells:profile')
        messages.add_message(request, level=messages.WARNING,
                             message='Errores en la creación del articulo')
        return render(request, self.template_name, {self.context_object_name: form})


# Update Item (Profile)
class UpdateItem(View):
    """
    Update item, view for updating items

    Args:
        View (object): View class

    Returns:
        Object: HTTP response
    """
    template_name = 'accounts/profile/update_item.html'
    model = ShopCellModel
    form_class = UpdateItemForm
    context_object_name = 'form'

    @method_decorator(login_required)
    def get(self, request: str, *args, **kwargs) -> HttpResponse:
        item = self.model.objects.get(pk=kwargs['pk'])
        form = self.form_class(initial={
            'model_name': item.model_name,
            'image': item.image,
            'price': item.price,
            'description': item.description,
        })
        return render(request, self.template_name, {self.context_object_name: form})

    @method_decorator(login_required)
    def post(self, request: str, *args, **kwargs) -> HttpResponse:
        user_item = self.model.objects.select_related('profile__user').defer(
            'model_name', 'image', 'description', 'price', 'created_date', 'slug', 'updated_date').get(pk=kwargs['pk'])
        if request.user.username == user_item.profile.user.username:
            form = self.form_class(
                request.POST, files=request.FILES, instance=user_item)
            if form.is_valid():
                if form.has_changed():
                    form.save()
                    messages.add_message(
                        request, level=messages.SUCCESS, message='Articulo actualizado con exito')
                return redirect('cells:profile')
            messages.add_message(request, level=messages.WARNING,
                                 message='Errores en la modificación del articulo')
        else:
            messages.add_message(
                request, level=messages.WARNING, message='Este no es tu articulo')
        return render(request, self.template_name, {self.context_object_name: self.form_class})


# Delete Item (Profile)
class DeleteItem(View):
    """
    Delete item, view for deleting items

    Args:
        View (object): View class

    Returns:
        Object: HTTP response
    """
    template_name = 'accounts/profile/delete_item.html'
    model = ShopCellModel
    form_class = DeleteItemForm
    context_object_name = 'form'

    @method_decorator(login_required)
    def get(self, request: str, *args, **kwargs) -> HttpResponse:
        form = self.form_class()
        return render(request, self.template_name, {self.context_object_name: form, 'pk': kwargs['pk']})

    @method_decorator(login_required)
    def post(self, request: str, *args, **kwargs) -> HttpResponse:
        form = self.form_class(request.POST)
        user_item = self.model.objects.select_related('profile__user').defer(
            'model_name', 'image', 'description', 'price', 'created_date', 'slug', 'updated_date').get(pk=kwargs['pk'])
        if request.user.username == user_item.profile.user.username:
            if form.is_valid():
                self.model.objects.filter(pk=kwargs['pk']).delete()
                messages.add_message(
                    request, level=messages.SUCCESS, message='Articulo eliminado con exito')
        else:
            messages.add_message(
                request, level=messages.WARNING, message='Este no es tu articulo')
        return HttpResponse('302')


# Profile (Profile)
class Profile(View):
    """
    Profile, view for showing profile user

    Args:
        View (object): View class

    Returns:
        Object: HTTP response
    """
    template_name = 'accounts/profile/cell_profile.html'
    model = ShopCellModel
    context_object_name = 'items'

    @method_decorator(login_required)
    def get(self, request: str, *args, **kwargs) -> HttpResponse:
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        search = request.GET.get('search')
        page = request.GET.get('page')
        # Sanetizando busqueda
        pattern = re.compile("[a-zA-Z0-9\s]+")
        if search is not None and pattern.search(search):
            items = self.model.objects.select_related('profile__user').defer(
                'description', 'slug', 'created_date').filter(
                profile=request.user.profile).filter(model_name__icontains=search)
        else:
            items = self.model.objects.select_related('profile__user').defer(
                'description', 'slug', 'created_date').filter(profile=request.user.profile)
        paginator = Paginator(items, 15)
        try:
            items = paginator.page(page)
        except PageNotAnInteger:
            items = paginator.page(1)
        except EmptyPage:
            if is_ajax:
                return HttpResponse('')
            items = paginator.page(paginator.num_pages)
        if is_ajax:
            return render(request, 'accounts/profile/user_items_list.html', {self.context_object_name: items})
        return render(request, self.template_name, {self.context_object_name: items})


# Profile Update (Profile)
class UpdateProfile(View):
    """
    Update profile, view for updating user profile

    Args:
        View (object): View class

    Returns:
        Object: HTTP response
    """
    template_name = 'accounts/profile/update_profile.html'
    form_class = UpdateUserForm
    model = User
    context_object_name = 'form'

    @method_decorator(login_required)
    def get(self, request: str, *args, **kwargs) -> HttpResponse:
        form = self.form_class(initial={
            'username': request.user.username,
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
            'phone': request.user.profile.phone,
            'image': request.user.profile.image,
            'address': request.user.profile.address
        })
        return render(request, self.template_name, {self.context_object_name: form})

    @method_decorator(login_required)
    def post(self, request: str, *args, **kwargs) -> HttpResponse:
        form = self.form_class(request.POST, files=request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            request.user.username = cd['username']
            request.user.first_name = cd['first_name']
            request.user.last_name = cd['last_name']
            #request.user.is_active = False
            if request.user.email == cd['email']:
                pass
            else:
                if self.model.objects.filter(email=cd['email']).exists():
                    messages.add_message(
                        request, level=messages.WARNING, message='El e-mail ya existe en nuestro sistema')
                    return render(request, self.template_name, {self.context_object_name: form})
                request.user.email = cd['email']

            request.user.profile.phone = cd['phone']
            request.user.profile.address = cd['address']
            request.user.profile.image = cd['image']
            try:
                request.user.save()
                request.user.profile.save()
                # email
                subject = 'ProC0d3 Actualización de perfil de usuario'
                message = render_to_string('email/email_profile.html', {
                    'domain': get_current_site(request),
                    'user': request.user.username,
                    'uid': urlsafe_base64_encode(force_bytes(request.user.pk)),
                    'token': default_token_generator.make_token(request.user),
                    'protocol': request.scheme,
                })
                #sendEmail(subject, message, cd['email'], cd['username'])
                messages.add_message(
                    request, level=messages.SUCCESS, message="Perfil actualizado.")
                # redireccion
                return redirect('cells:logout')
            except:
                messages.add_message(
                    request, level=messages.WARNING, message='El nombre de usuario ya existe')
        return render(request, self.template_name, {self.context_object_name: form})


# Profile Delete (Profile)
class DeleteProfile(View):
    """
    Delete profile, view for deleting user profile

    Args:
        View (object): View class

    Returns:
        Object: HTTP response
    """
    template_name = 'accounts/profile/delete_account.html'
    model = User
    form_class = DeleteUserForm
    context_object_name = 'form'

    @method_decorator(login_required)
    def get(self, request: str, *args, **kwargs) -> HttpResponse:
        form = self.form_class()
        return render(request, self.template_name, {self.context_object_name: form})

    @method_decorator(login_required)
    def post(self, request: str, *args, **kwargs) -> HttpResponse:
        form = self.form_class(request.POST)
        if form.is_valid():
            self.model.objects.filter(username=request.user.username).delete()
            messages.add_message(
                request, level=messages.SUCCESS, message='Su cuenta fue eliminada')
            return HttpResponse('302')


# Profile Canche password (Profile)
class ChangePasswordProfile(View):
    """
    Change password profile, view for chaging user password

    Args:
        View (object): View class

    Returns:
        Object: HTTP response
    """
    form_class = ChangePasswordForm
    context_object_name = 'form'
    template_name = 'accounts/registration/change_password.html'

    @method_decorator(login_required)
    def get(self, request: str, *args, **kwargs) -> HttpResponse:
        form = self.form_class()
        return render(request, self.template_name, {self.context_object_name: form})

    @method_decorator(login_required)
    def post(self, request: str, *args, **kwargs) -> HttpResponse:
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if authenticate(request, username=request.user.username, password=cd['currentpassword']) is not None:
                request.user.set_password(cd['newpassword'])
                #request.user.is_active = False
                request.user.save()
                # email
                subject = 'ProC0d3 Cambio de password de usuario'
                message = render_to_string('email/email_password.html', {
                    'domain': get_current_site(request),
                    'user': request.user.username,
                    'uid': urlsafe_base64_encode(force_bytes(request.user.pk)),
                    'token': default_token_generator.make_token(request.user),
                    'protocol': request.scheme,
                })
                #sendEmail(subject, message, request.user.email, request.user.username)
                messages.add_message(
                    request, level=messages.SUCCESS, message='Clave cambiada con exito')
                return HttpResponse('302')
            else:
                messages.add_message(
                    request, level=messages.WARNING, message='La clave actual no es válida')
        else:
            messages.add_message(
                request, level=messages.WARNING, message='Las claves no concuerdan')
        return render(request, self.template_name, {self.context_object_name: form})


# Restore Password (Profile)
class RestorePassword(View):
    """
    Restore password, view for restoring passowrd

    Args:
        View (object): View class

    Returns:
        Object: HTTP response
    """
    form_class = RestorePassowrdForm
    template_name = 'accounts/registration/restore_password.html'
    context_object_name = 'form'
    model = User

    def get(self, request: str, *args, **kwargs) -> HttpResponse:
        form = self.form_class()
        return render(request, self.template_name, {self.context_object_name: form})

    def post(self, request: str, *args, **kwargs) -> HttpResponse:
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            try:
                user = self.model.objects.get(email=cd['email'])
                #user.is_active = False
                # hacerlo mas fuerte para producción
                # user.set_password('password1')
                # user.save()
                # email
                subject = 'ProC0d3 Restablecimiento de credenciales'
                message = render_to_string('email/email_restored.html', {
                    'domain': get_current_site(request),
                    'user': user.username,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': default_token_generator.make_token(user),
                    'protocol': request.scheme,
                    'password': 'password1',
                })
                #sendEmail(subject, message, cd['email'], user.username)
                messages.add_message(
                    request, level=messages.SUCCESS, message='Funcionalidad no implementada')
                return HttpResponse('302')
            except:
                messages.add_message(request, level=messages.WARNING,
                                     message='El e-mail no es válido en nuestro sistema')
        return render(request, self.template_name, {self.context_object_name: form})
