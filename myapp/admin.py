from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Property, PropertyCategory, PropertySector, PropertyFacing, PropertyImages, Country, Province, City ,RolePermission , UserRole,RoleCode,PermissionTypeChoices,PermissionType,Password, User

#Register your models here.

admin.site.register(Property)
admin.site.register(PropertyCategory)
admin.site.register(PropertySector)
admin.site.register(PropertyFacing)
admin.site.register(PropertyImages)
admin.site.register(Country)
admin.site.register(Province)
admin.site.register(City)
admin.site.register(RolePermission)
admin.site.register(UserRole)
admin.site.register(RoleCode)
admin.site.register(PermissionType)
#admin.site.register(PermissionTypeChoices)
admin.site.register(Password)
admin.site.register(User)