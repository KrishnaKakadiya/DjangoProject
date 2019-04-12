from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from enum import Enum
import datetime

# Create your models here.


class PermissionTypeChoices(Enum):
    Read = 'read'
    Write = 'write'
    Update = 'update'
    Delete = 'delete'

class Country(models.Model):
    countryName = models.CharField(max_length=100)

    def __str__(self):  # __unicode__ on Python 2
        return self.countryName


class Province(models.Model):
    countryName = models.ForeignKey(Country, on_delete=models.CASCADE)
    provinceName = models.CharField(max_length=100)

    def __str__(self):  # __unicode__ on Python 2
        return self.provinceName


class City(models.Model):
    cityName = models.CharField(max_length=100)
    countryName = models.ForeignKey(Country, on_delete=models.CASCADE)
    provinceName = models.ForeignKey(Province, on_delete=models.CASCADE)

    def __str__(self):  # __unicode__ on Python 2
        return self.cityName


PROPERTY_FACING = ("North", "South", "East", "West", "Other")


class PropertyFacing(models.Model):
    propertyFacing = models.CharField(choices=[(x, str(x)) for x in PROPERTY_FACING], max_length=20)

    def __str__(self):  # __unicode__ on Python 2
        return self.propertyFacing


PROPERTY_SECTOR = ("Private", "Residential", "Commercial", "Government", "Rural", "Other")


class PropertySector(models.Model):
    propertySector = models.CharField(choices=[(x, str(x)) for x in PROPERTY_SECTOR], max_length=20)

    def __str__(self):  # __unicode__ on Python 2
        return self.propertySector


PROPERTY_CATEGORY = ("Single House", "Attached House", "Town House", "Apartment", "Store", "Farm", "Factory", "Mall", "Building", "Other")


class PropertyCategory(models.Model):
    propertyCategory = models.CharField(choices=[(x, str(x)) for x in PROPERTY_CATEGORY], max_length=20)

    def __str__(self):  # __unicode__ on Python 2
        return self.propertyCategory


class Property(models.Model):
    propertyID = models.IntegerField()
    propertyTitle = models.CharField(max_length=100)
    propertyCategory = models.ForeignKey(PropertyCategory, on_delete=models.CASCADE)
    propertySector = models.ForeignKey(PropertySector, on_delete=models.CASCADE)
    propertyFacing = models.ForeignKey(PropertyFacing, on_delete=models.CASCADE)
    propertyCountry = models.ForeignKey(Country, on_delete=models.CASCADE)
    propertyProvince = models.ForeignKey(Province, on_delete=models.CASCADE)
    propertyCity = models.ForeignKey(City, on_delete=models.CASCADE)
    propertyStreet = models.CharField(max_length=200)
    propertyPostalCode = models.CharField(max_length=200)
    propertyStreetNumber = models.CharField(max_length=200)
    propertyConstructionDate = models.DateField()
    propertyRegistrationDate = models.DateField()
    propertyNoOfHalls = models.IntegerField()
    propertyNoOfRooms = models.IntegerField()
    propertyNoOfBathRooms = models.FloatField()
    propertyNoOfFloors = models.IntegerField()
    propertyTotalArea = models.FloatField()
    propertyAskingPrice = models.DecimalField(max_digits=10,decimal_places=2)
    propertySellingPrice = models.DecimalField(max_digits=10,decimal_places=2)
    memberName = models.CharField(max_length=100)

    def __str__(self):  # __unicode__ on Python 2
        return self.propertyID

    def __str__(self):  # __unicode__ on Python 2
        return self.propertyTitle

    def __str__(self):  # __unicode__ on Python 2
        return self.propertyCategory

    def __str__(self):  # __unicode__ on Python 2
        return self.propertySector

    def __str__(self):  # __unicode__ on Python 2
        return self.propertyFacing

    def __str__(self):  # __unicode__ on Python 2
        return self.propertyCountry

    def __str__(self):  # __unicode__ on Python 2
        return self.propertyProvince

    def __str__(self):  # __unicode__ on Python 2
        return self.propertyCity

    def __str__(self):  # __unicode__ on Python 2
        return self.propertyStreet

    def __str__(self):  # __unicode__ on Python 2
        return self.propertyPostalCode

    def __str__(self):  # __unicode__ on Python 2
        return self.propertyStreetNumber

    def __str__(self):  # __unicode__ on Python 2
        return self.propertyConstructionDate

    def __str__(self):  # __unicode__ on Python 2
        return self.propertyRegistrationDate

    def __str__(self):  # __unicode__ on Python 2
        return self.propertyNoOfHalls

    def __str__(self):  # __unicode__ on Python 2
        return self.propertyNoOfRooms

    def __str__(self):  # __unicode__ on Python 2
        return self.propertyNoOfBathRooms

    def __str__(self):  # __unicode__ on Python 2
        return self.propertyNoOfFloors

    def __str__(self):  # __unicode__ on Python 2
        return self.propertyTotalArea

    def __str__(self):  # __unicode__ on Python 2
        return self.propertyAskingPrice

    def __str__(self):  # __unicode__ on Python 2
        return self.propertySellingPrice

    def __str__(self):  # __unicode__ on Python 2
        return self.memberName


class PropertyImages(models.Model):
    propertyID = models.ForeignKey(Property, on_delete=models.CASCADE)
    propertyImage = models.ImageField(upload_to = 'photo/', blank=True, null=True)
    propertyImageID = models.CharField(max_length=200)
    propertyImageDescription = models.CharField(max_length=500)

    def __str__(self):  # __unicode__ on Python 2
        return self.propertyID

    def __str__(self):  # __unicode__mak on Python 2
        return self.propertyImage

    def __str__(self):  # __unicode__ on Python 2
        return self.propertyImageID

    def __str__(self):  # __unicode__ on Python 2
        return self.propertyImageDescription


class User(models.Model):

    def __str__(self):
        return str(self.firstName + " " + self.lastName)


    firstName = models.CharField(max_length=25)
    lastName = models.CharField(max_length=25)
    email = models.CharField(max_length=55)
    isActive = models.BooleanField(null=False, default=True)

    class Meta:
        db_table = 'myapp_user'


class Password(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    username = models.CharField(max_length=25)
    encryptedPassword = models.CharField(max_length=255)
    salt = models.CharField(max_length=255)
    userAccountExpiryDate = models.DateField()
    passwordMustChanged = models.DateTimeField(default=(datetime.datetime.now() + datetime.timedelta(3 * 3565 / 12)),
                                               blank=False)
    passwordReset = models.BooleanField(default=False, blank=False)

    class Meta:
        db_table = 'myapp_password'


class RoleCode(models.Model):
    def __str__(self):
        return self.roleName

    roleName = models.CharField(max_length=55)
    code = models.ManyToManyField(User, through='UserRole')

    class Meta:
        db_table = "myapp_rolecode"


class UserRole(models.Model):

    def __str__(self):
        return str(self.role.code)

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='roles')
    role = models.ForeignKey(RoleCode, on_delete=models.CASCADE, related_name='role_code')
    date_assigned = models.DateField(auto_now=True)

    class Meta:
        unique_together = ("user", "role")
        db_table = "myapp_userrole"


class PermissionType(models.Model):

    def __str__(self):
        return self.name

    name = models.CharField(max_length=100, choices=[(tag.value, tag.name) for tag in PermissionTypeChoices],
                            default=PermissionTypeChoices.Read, unique=True)
    class Meta:
        db_table = 'myapp_permissiontype'


class RolePermission(models.Model):

    def __str__(self):
        return "%s : %s" % (self.code, ', '.join([permission.name for permission in self.permissions.all()]))

    sysFeature = models.CharField(max_length=75)
    code = models.ForeignKey(RoleCode, on_delete=models.CASCADE)
    permissions = models.ManyToManyField(PermissionType)

    class Meta:
        db_table = "myapp_rolepermission"
        ordering = ['id']
