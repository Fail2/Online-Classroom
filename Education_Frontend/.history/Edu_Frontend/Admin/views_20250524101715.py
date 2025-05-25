from django.shortcuts import render,redirect
import requests
from .forms import AdminRegisterForm,AdminLoginForm
# Create your views here.

BACKEND_URL = ''

def admin_login(request):
    form = AdminLoginForm(request.POST or None)
