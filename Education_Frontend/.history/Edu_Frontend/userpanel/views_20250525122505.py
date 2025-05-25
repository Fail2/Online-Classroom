from django.shortcuts import render
from .forms import UserLoginForm,UserRegisterForm
# Create your views here.

def common_login(request):
    form = UserLoginForm
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            