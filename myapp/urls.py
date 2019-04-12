"""S1_G2_Fall2018 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from myapp import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf.urls import include, url
from django.urls import path, re_path



urlpatterns = [

    path('', views.home, name='home'),
    path('contact', views.contact, name='contact'),
    path('signin', views.signin, name='signin'),
    path('aboutus', views.aboutus, name='aboutus'),
    path('searchProperty', views.searchProperty, name='searchProperty'),
    path('advertiseProperty', views.advertiseProperty, name='advertiseProperty'),
    path('propertyDetail', views.propertyDetail, name='propertyDetail'),
    path('sportequip', views.sportequip, name='sportequip'),

    path('users', views.signin, name='users'),
    path('users/', views.UsersView.as_view(), name='users'),
    path('users/activate/', views.activate_user, name='user-activate'),
    path('users/add/', views.user_create_view, name='add-user'),
    re_path(r'^users/edit/(?P<user_id>[0-9]+)/$', views.user_edit_view, name='update-user'),
    re_path(r'^users/delete/(?P<user_id>[0-9]+)/$', views.user_delete, name='user-delete'),

    path('roles/', views.RolesListView.as_view(), name='roles'),
    path('roles/add/', views.role_create_view, name='add-role'),
    re_path(r'^roles/edit/(?P<role_id>[0-9]+)/$', views.role_update_view, name='update-role'),
    re_path(r'^roles/delete/(?P<role_id>[0-9]+)/$', views.role_delete_view, name='delete-role'),

    path('features/', views.FeaturesListView.as_view(), name='features'),
    path('features/add/', views.create_feature_view, name='add-feature'),
    re_path(r'^features/edit/(?P<role_permission_id>[0-9]+)/$', views.update_feature_view, name='update-feature'),
    re_path(r'^feature/delete/(?P<role_permission_id>[0-9]+)/$', views.feature_delete_view, name='delete-feature')


]
