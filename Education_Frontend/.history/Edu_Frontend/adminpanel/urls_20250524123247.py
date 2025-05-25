from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [
    path('admin-login/',views.admin_login,name = 'admin_login'),
    path('register/',views.admin_register,name = 'admin_register'),
]
