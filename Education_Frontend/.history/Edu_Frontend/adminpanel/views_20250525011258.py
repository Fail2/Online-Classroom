from django.shortcuts import render,redirect
import requests
from .forms import AdminRegisterForm,AdminLoginForm
# Create your views here.

BACKEND_URL = 'http://127.0.0.1:8000/api/'  # Backend URL

def admin_login(request):
    form = AdminLoginForm(request.POST or None)
    if request.method =='POST' and form.is_valid():
        response = requests.post(BACKEND_URL + 'token/',data ={
            'username': form.cleaned_data['username'],
            'password': form.cleaned_data['password'],
        })
        if response.status_code == 200:
            tokens = response.json()
            request.session['access'] = tokens['access']
            return redirect('admin-dashboard')  # target dashboard
        else :
            print("🚨 Backend Error:", response.status_code, response.text)  # 👈 ADD THIS
            error = "Invalid credentials"
    return render(request,'adminpanel/login.html',{'form':form})   
     
def admin_register(request):
    form = AdminRegisterForm(request.POST or None)
    error = None
    if request.method == 'POST' and form.is_valid():
        response = requests.post(BACKEND_URL + 'accounts/users/', json ={
            'username': form.cleaned_data['username'],
            'email': form.cleaned_data['email'],
            'password': form.cleaned_data['password'],
            'role':'ADMIN'
        })

        if response.status_code in [200,201]:
            return redirect('admin_login')
        else: 
            print("🚨 Backend Error:", response.status_code, response.text)  # 👈 ADD THIS
            error = 'Somethings wrong!'

    return render(request,'adminpanel/register.html', {'form':form})

def admin_dashboard(request):
    return render(request, 'adminpanel/dashboard.html')

def teacher_list(request):
    users = requests.get(BACKEND_URL + 'accounts/users/').json()
    courses = request.get(BACKEND_URL + 'courses/courses').json()
    teachers = [user for user in users if]
    return render(request, 'adminpanel/teachers.html')

def student_list(request):
    return render(request, 'adminpanel/students.html')

def course_list(request):
    return render(request, 'adminpanel/courses.html')

def admin_logout(request):
    # You can handle token removal or redirect to login here
    return redirect('admin_login')
