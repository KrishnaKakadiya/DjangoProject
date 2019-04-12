from django import forms
from myapp.models import RolePermission, PermissionType
from django.utils.translation import gettext_lazy as _


class CreateFeatureForm(forms.ModelForm):
    permissions = forms.ModelMultipleChoiceField(queryset=PermissionType.objects.all(),
                                                 to_field_name='name', required=False)

    class Meta:
        model = RolePermission
        fields = ['sysFeature', 'code', 'permissions']
        labels = {
            'sysFeature': _('System Feature'),
            'code': _('Role'),
            'permissions': _('Permissions')
        }