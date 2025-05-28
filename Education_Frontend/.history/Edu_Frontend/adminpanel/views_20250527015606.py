from django.shortcuts import render,redirect
import requests
from django.contrib.auth import logout
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
            return redirect('admin-login')
        else: 
            print("🚨 Backend Error:", response.status_code, response.text)  # 👈 ADD THIS
            error = 'Somethings wrong!'

    return render(request,'adminpanel/register.html', {'form':form})

def admin_dashboard(request):
    return render(request, 'adminpanel/dashboard.html')

def teacher_list(request):
    users = requests.get(BACKEND_URL + 'accounts/users/').json()
    courses = requests.get(BACKEND_URL + 'courses/courses').json()
    # Filter teachers
    teachers = [user for user in users if user.get('role')== 'TEACHER']
    
    # Add course count manually
    for teacher in teachers:
        teacher['course_count'] = [ course for course in courses if course.get('teacher')== teacher.get('id')]
    return render(request, 'adminpanel/teachers.html', {'teachers': teachers})

def student_list(request):
    users = requests.get(BACKEND_URL + 'accounts/users/').json()
    courses = requests.get(BACKEND_URL + 'courses/courses').json()
    # Filter teachers
    students = [user for user in users if user.get('role')== 'STUDENTS']
    
    # Add course count manually
    for student in students:
        student['enrolled_course_count'] = len([ course for course in courses if course.get('student')== student.get('id')])
    return render(request, 'adminpanel/students.html', {'students':students})

def course_list(request):
    courses = requests.get(BACKEND_URL + 'courses/courses').json()
    return render(request, 'adminpanel/courses.html', {'courses':courses})

def admin_logout(request):
    # You can handle token removal or redirect to login here
    logout(request)
    return redirect('admin-login')
