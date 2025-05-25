from django.shortcuts import render
from .forms import UserLoginForm,UserRegisterForm
# Create your views here.

def common_login(request):
    if