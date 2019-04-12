from django.forms import ModelForm
from myapp.models import RoleCode
from django.utils.translation import gettext_lazy as _


class CreateRoleForm(ModelForm):
    class Meta:
        model = RoleCode
        fields = ['roleName']
        labels = {
            'roleName': _('Role Name'),

        }


class DeleteRoleForm(ModelForm):
    class Meta:
        model = RoleCode
        fields = ['roleName']
