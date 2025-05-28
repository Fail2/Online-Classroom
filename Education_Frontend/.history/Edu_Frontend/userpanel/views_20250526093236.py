from django.shortcuts import render,redirect,HttpResponse
from .forms import UserLoginForm,UserRegisterForm
import requests
from django.http import HttpResponse
from .utils import api_request_with_refresh

# Create your views here.

def user_login(request):
    form = UserLoginForm
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            role = form.cleaned_data['role']
            response = requests.post('http://127.0.0.1:8000/api/token/', json=data)
            if response.status_code ==200:
                tokens = response.json()
                print(tokens)
                request.session['access'] = tokens ['access']
                request.session['refresh'] = tokens['refresh']
                request.session['user_id'] = tokens ['user']['id']
                if role == 'TEACHER':
                    return redirect('teacher-home')
                else: return redirect('student-home')

            else :print("🚨 Backend Error:", response.status_code, response.text)
    return render (request,'user_login.html', {'form':form})

def user_register(request):
    form = UserRegisterForm
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            role = form.cleaned_data['role']
            response = requests.post('http://127.0.0.1:8000/api/accounts/users/', json=data)
            if response.status_code == 201:
                return redirect('user-login')
            else :print("🚨 Backend Error:", response.status_code, response.text)
    return render (request,'user_register.html', {'form':form})    
        
def user_logout(request):
    request.session.flush()
    return redirect('user-login')        


def teacher_home(request):
    teacher_id = request.session.get('user_id')
    url = 'http://127.0.0.1:8000/api/courses/courses/'
    response = api_request_with_refresh(request, 'get', url)

    if isinstance(response, HttpResponse):  # redirect if token failed
        return response
    if isinstance(response,HttpResponse):
        return response
    if response.status_code == 200:
        all_courses = response.json()
        courses = [course for course in all_courses if course.get('teacher') == teacher_id]
        return render(request, 'teacher/teacher_dashboard.html', {'courses': courses})
    else:
        return HttpResponse(f"Error: {response.status_code}")

            

def student_home(request):
    return  HttpResponse('Welcome to student home!')    