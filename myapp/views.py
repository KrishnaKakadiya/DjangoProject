from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import PropertyImages
# from .models import User
from myapp.models import RoleCode
from django.contrib.auth import authenticate, login
import logging
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.views import generic
from django.urls import reverse_lazy
from django.views.generic import DeleteView
from django.http import HttpResponseRedirect
from myapp.forms.roles import CreateRoleForm, DeleteRoleForm
from myapp.forms.users import ActiveStatusForm, UserFormWithRelatedFields
from myapp.models import User, Password, RoleCode, UserRole
from django.contrib.auth.hashers import make_password
import datetime
from django.core.paginator import Paginator
from myapp.forms.features import CreateFeatureForm
from myapp.models import RolePermission
from django.contrib.auth.forms import PasswordChangeForm
# Create your views here.

logger = logging.getLogger(__name__)



def contact(request):
    return render(request, 'home/contactUs.html')

def home(request):
    obj = PropertyImages.objects.all()
    context = {
        'object': obj
    }
    return render(request, 'home/home.html', context)


def aboutus(request):
    return render(request, 'home/aboutus.html')


def searchProperty(request):
    return render(request, 'home/searchProperty.html')


def advertiseProperty(request):
    return render(request, 'home/advertiseProperty.html')


def propertyDetail(request):
    return render(request, 'home/propertyDetail.html')


def sportequip(request):
    return render(request, 'home/sportequip.html')


def user(request):
    return render(request, 'home/user/userBase.html')


def signin(request):
    if request.POST:
        password = request.POST['password']
        username = request.POST['email']
        return redirect('users')
        # if User.objects.filter(username=username).exists():
        #     user = authenticate(username=username, password=password)
        #
        #     if user is not None:
        #         login(request, user)
        #         return redirect('users')
        #
        #     else:
        #         response = render(request, 'home/signin.html', {'error_message': "Wrong password"})
        #         return response
        # else:
        #     response = render(request, 'home/signin.html')
        #     return response

    else:
        return render(request, 'home/signin.html')


def activate_user(request):
    if request.POST:
        user_id = request.POST['user_id']
        status = request.POST['status']
        if user_id and status:
            user = User.objects.filter(id=user_id).first()
            status_form = ActiveStatusForm(request.POST)
            if status_form.is_valid():
                user.isActive = status
                user.save()
            return redirect('/users')


def user_edit_view(request, user_id):
    user = User.objects.get(id=user_id)
    form = UserFormWithRelatedFields(request.POST or None, instance=user)

    if request.POST:
        if form.is_valid():
            user = form.save(commit=False)
            new_password = request.POST['password']
            new_roles = request.POST.getlist('role')
            if new_password:
                password = Password.objects.filter(user_id=user_id).first()
                password.password = make_password(new_password)
                password.save()

            if new_roles:
                # delete prev roles
                UserRole.objects.filter(user_id=user.id).delete()

                # add new roles
                roles = RoleCode.objects.filter(roleName__in=new_roles)
                for role in roles:
                    user_role = UserRole(user_id=user.id, role_id=role.id)
                    user_role.save()
                    user.roles.add(user_role)
                    user.save()

                form.save_m2m()
            user.save()
            return redirect('/users/')
            #return redirect('/users/edit/' + user_id)
    else:
        if form.is_valid():
            form.save()
            return redirect('/users/')

        context = {
            'form': form,
            'isEdit': True,
            'id': user.id
        }
        return render(request, 'home/user/user_form.html', context)


def user_create_view(request):
    form = UserFormWithRelatedFields(request.POST or None)

    if request.POST:
        if form.is_valid():
            user = form.save()
            new_password = request.POST['password']
            new_role = request.POST['role']

            if new_password:
                password = Password()
                password.password = make_password(new_password)
                password.userAccountExpiryDate = datetime.date.today() + datetime.timedelta(30)
                password.user = user
                password.save()

            if new_role:
                role = RoleCode.objects.filter(roleName=new_role).first()
                user_role = UserRole()
                user_role.user = user
                user_role.role = role
                user_role.save()

            return redirect('/users/')
    else:
        if form.is_valid():
            form.save()
            return redirect('/users/')

        context = {
            'form': form,
            'isEdit': False
        }
        return render(request, 'home/user/user_form.html', context)

def user_delete(request, user_id):
    form = User.objects.filter(id=user_id)
    if form:
        form.delete()
    return redirect('/users/')
    # form = User.objects.filter(id = user_id)
    # #UserForm(request.POST or None,instance=form[0])
    # if request.method == 'POST':
    #     form.delete()
    #     return redirect('/users')
    # context = {
    #     'form': form,
    #     'isEdit': False
    # }
    # return render(request, 'home/user/user_confirm_delete.html', context)

class UsersView(generic.ListView):
    template_name = 'home/user/users.html'
    context_object_name = 'users'

    def get_queryset(self):
        users_list = User.objects.prefetch_related('roles').all().order_by('id')
        paginator = Paginator(users_list, 10)
        page = self.request.GET.get('page')
        return paginator.get_page(page)


class RolesListView(generic.ListView):
    template_name = 'home/user/roles.html'
    context_object_name = 'roles'

    def get_queryset(self):
        return RoleCode.objects.all()


class RoleDelete(DeleteView):
    model = RoleCode
    success_url = reverse_lazy('roles')


def role_create_view(request):
    form = CreateRoleForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('roles')

    context = {
        'form': form,
        'isEdit': False
    }
    return render(request, 'home/user/role_form.html', context)


def role_update_view(request, role_id):
    role = RoleCode.objects.get(id=role_id)
    form = CreateRoleForm(request.POST or None, instance=role)
    if form.is_valid():
        form.save()
        return redirect('roles')

    context = {
        'form': form,
        'isEdit': True
    }
    return render(request, 'home/user/role_form.html', context)


def role_delete_view(request, role_id):
    role = RoleCode.objects.filter(id=role_id)

    if role:
        role.delete()
        return HttpResponseRedirect('/roles/')


class FeaturesListView(generic.ListView):
    template_name = 'home/user/features.html'
    context_object_name = 'features'

    def get_queryset(self):
        permissions = RolePermission.objects.select_related('code').all()
        paginator = Paginator(permissions, 9)
        page = self.request.GET.get('page')
        return paginator.get_page(page)


def create_feature_view(request):
    form = CreateFeatureForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('features')

    context = {
        'form': form,
        'isEdit': False
    }
    return render(request, 'home/user/feature_form.html', context)


def update_feature_view(request, role_permission_id):
    feature = RolePermission.objects.get(id=role_permission_id)
    form = CreateFeatureForm(request.POST or None, instance=feature)
    if form.is_valid():
        form.save()
        return redirect('features')

    context = {
        'form': form,
        'isEdit': True
    }
    return render(request, 'home/user/feature_form.html', context)


def feature_delete_view(request, role_permission_id):
    feature = RolePermission.objects.filter(id=role_permission_id)

    if feature:
        feature.delete()
        return HttpResponseRedirect('/features/')
