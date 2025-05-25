from django.shortcuts import render
from .forms import UserLoginForm,UserRegisterForm
import requests
# Create your views here.

def common_login(request):
    form = UserLoginForm
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            response = requests.post('http://127.0.0.1:8000/api/token/', json=data)
            if response.status_code ==200:
                tokens = response.json()
                print(tokens)
                request.session['access'] = tokens ['access']
                request.session['refresh'] = tokens['refresh']
                request.session['user_id'] = tokens['user']['id']
                

            else :print("🚨 Backend Error:", response.status_code, response.text)
    return render (request,login.html, {'form':form})        