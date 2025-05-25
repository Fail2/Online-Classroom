from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [
    path('login/',views.admin_login,name = 'admin-login'),
    path('register/',views.admin_register,name = 'admin-register'),
]
