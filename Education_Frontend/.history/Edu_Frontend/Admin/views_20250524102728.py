from django.shortcuts import render,redirect
import requests
from .forms import AdminRegisterForm,AdminLoginForm
# Create your views here.

BACKEND_URL = 'http://127.0.0.1:8000/api/'  # Backend URL

def admin_login(request):
    form = AdminLoginForm(request.POST or None)
    if request.method =='POST' and form.is_valid():
        response = requests.post(BACKEND_URL + 'token/',data ={
            'username':form.cleaned_data['username'],
            'password':
        })