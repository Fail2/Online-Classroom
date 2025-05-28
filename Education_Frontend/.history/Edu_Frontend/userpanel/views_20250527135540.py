from django.shortcuts import render,redirect,HttpResponse
from .forms import UserLoginForm,UserRegisterForm
import requests
from django.http import FileResponse, HttpResponse, HttpResponseForbidden
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


def add_course(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        teacher_id = request.session.get('user_id')

        course_data = {
            'title': title,
            'description': description,
            'teacher': teacher_id
        }

        response = api_request_with_refresh(request, 'POST', 'http://127.0.0.1:8000/api/courses/courses/', data=course_data)

        if isinstance(response, HttpResponse):  # token refresh or redirect
            return response

        if response.status_code == 201:
            return redirect('teacher-home')
        else:
            return HttpResponse(f'Failed to create course. Status: {response.status_code}')

    return render(request, 'teacher/add_course.html')


def edit_course(request, course_id):
    # Get existing course info
    get_url = f'http://127.0.0.1:8000/api/courses/courses/{course_id}/'
    response = api_request_with_refresh(request, 'GET', get_url)

    if isinstance(response, HttpResponse):
        return response

    if response.status_code != 200:
        return HttpResponse(f"Failed to load course. Error: {response.status_code}")

    course = response.json()

    if request.method == 'POST':
        data = {}
        title = request.POST.get('title')
        description = request.POST.get('description')

        if title and title != course.get('title'):
            data['title'] = title

        if description and description != course.get('description'):
            data['description'] = description

        if data:
            patch_url = f'http://127.0.0.1:8000/api/courses/courses/{course_id}/'
            patch_response = api_request_with_refresh(request, 'PATCH', patch_url, data=data)

            if isinstance(patch_response, HttpResponse):
                return patch_response

            if patch_response.status_code in [200, 202]:
                return redirect('teacher-home')
            else:
                return HttpResponse(f"Failed to update course. Error: {patch_response.status_code}")
        else:
            return redirect('teacher-home')  # Nothing changed

    return render(request, 'teacher/edit_course.html', {'course': course})

def delete_course(request, course_id):
    teacher_id = request.session.get('user_id')
    if not teacher_id:
        return redirect('user-login')  # session expired or not logged in

    url = f'http://127.0.0.1:8000/api/courses/courses/{course_id}/'
    
    # Send DELETE request using helper function
    response = api_request_with_refresh(request, 'DELETE', url)

    if isinstance(response, HttpResponse):  # e.g., redirect to login
        return response
    
    if response.status_code == 204:
        return redirect('teacher-home')  # success
    else:
        return HttpResponse(f'Failed to delete course. Status code: {response.status_code}', status=response.status_code)
    
def course_detail(request, course_id):

    teacher_id = request.session.get('user_id')

    # 1. Get course details
    course_url = f'http://127.0.0.1:8000/api/courses/courses/{course_id}/'
    course_response = api_request_with_refresh(request, 'GET', course_url)

    if isinstance(course_response, HttpResponse):  # e.g., redirect to login
        return course_response

    try:
        course_data = course_response.json()
    except ValueError:
        return HttpResponse("Failed to parse course details. Server did not return JSON.", status=500)
    print("course-data:",course_data)
    # # Optional security check
    # if course_data.get('teacher') != teacher_id:
    #     return redirect('teacher-home')

    # 2. Get course files
    files_url = 'http://127.0.0.1:8000/api/courses/CourseFiles/'
    files_response = api_request_with_refresh(request, 'GET', files_url)

    if isinstance(files_response, HttpResponse):  # redirect if token refresh failed
        return files_response

    all_files = files_response.json()
    course_files = [file for file in all_files if str(file.get('course')) == str(course_id)]

    return render(request, 'teacher/course_detail.html', {
        'course': course_data,
        'files': course_files
    })

def add_file(request,course_id):
    if request.method == 'POST':
        data ={
            'title': request.POST.get('title'),
            'course':course_id,
        }
        files ={
            'file':request.FILES.get('file')
        }
        file_upload_url = 'http://127.0.0.1:8000/api/courses/CourseFiles/'
        response = api_request_with_refresh(request,'POST',file_upload_url,data=data,files=files)
        if isinstance(response,HttpResponse):
            return response
        
        if response.status_code == 201:
            return redirect('course-detail',course_id=course_id)
        else:
            return HttpResponse(f'Upload failed. Status: {response.status_code},{response.text}')
    return render(request,'teacher/add_file.html',{'course_id':course_id})  

def edit_file(request, file_id, course_id):
    # Get existing file info
    get_url = f'http://127.0.0.1:8000/api/courses/CourseFiles/{file_id}/'
    response = api_request_with_refresh(request, 'GET', get_url)

    if isinstance(response, HttpResponse):
        return response
    if response.status_code != 200:
        return HttpResponse(f"Failed to load file data. Error: {response.status_code}")

    file_data = response.json()

    if request.method == 'POST':
        updated_data = {}
        title = request.POST.get('title')
        uploaded_file = request.FILES.get('file')

        # Only update title if it's not empty and different
        if title and title != file_data.get('title'):
            updated_data['title'] = title

        # Only update file if a new file is uploaded
        files = {'file': uploaded_file} if uploaded_file else None

        # If there's anything to update
        if updated_data or files:
            patch_url = f'http://127.0.0.1:8000/api/courses/CourseFiles/{file_id}/'
            patch_response = api_request_with_refresh(
                request, 'PATCH', patch_url, data=updated_data, files=files
            )

            if isinstance(patch_response, HttpResponse):
                return patch_response
            if patch_response.status_code in [200, 202]:
                return redirect('course-detail', course_id=course_id)
            else:
                return HttpResponse(f"Failed to update file. Error: {patch_response.status_code}")
        else:
            # Nothing was changed, redirect back
            return redirect('course-detail', course_id=course_id)

    return render(request, 'teacher/edit_file.html', {
        'file_data': file_data,
        'course_id': course_id,
    })  
    

def delete_file(request, file_id, course_id):
    delete_url = f'http://127.0.0.1:8000/api/courses/CourseFiles/{file_id}/'
    response = api_request_with_refresh(request, 'DELETE', delete_url)

    if isinstance(response, HttpResponse):
        return response

    if response.status_code in [200, 204]:  # 204 is typical for successful DELETE
        return redirect('course-detail', course_id=course_id)
    else:
        return HttpResponse(f"Failed to delete file. Error: {response.status_code}")


def student_home(request):
    student_id = request.session.get('user_id')

    if not student_id:
        return redirect('login')  # Or your login view name

    # ✅ Handle enrollment (POST request)
    if request.method == 'POST':
        course_id = request.POST.get('course_id')
        enrollment_data = {
            'student': student_id,
            'course': course_id
        }

        enroll_response = api_request_with_refresh(
            request,
            'POST',
            'http://127.0.0.1:8000/api/courses/enrollments/',
            data=enrollment_data
        )

        if isinstance(enroll_response, HttpResponse):
            return enroll_response

        if enroll_response.status_code == 201:
            return redirect('student-home')
        else:
            return HttpResponse("Enrollment failed.")

    # ✅ Step 1: Get all courses
    courses_response = api_request_with_refresh(request, 'GET', 'http://127.0.0.1:8000/api/courses/courses/')
    if isinstance(courses_response, HttpResponse):
        return courses_response

    if courses_response.status_code != 200:
        return HttpResponse("Failed to fetch courses")

    courses = courses_response.json()

    # ✅ Step 2: Get student's enrollments
    enrollments_response = api_request_with_refresh(
        request, 
        'GET', 
        f'http://127.0.0.1:8000/api/courses/enrollments/student/{student_id}/'
    )
    if isinstance(enrollments_response, HttpResponse):
        return enrollments_response

    if enrollments_response.status_code != 200:
        return HttpResponse("Failed to fetch enrollments")

    enrollments = enrollments_response.json()
    enrolled_course_ids = {enrollment['course'] for enrollment in enrollments}

    # ✅ Step 3: Add enrollment status to courses
    for course in courses:
        course['is_enrolled'] = course['id'] in enrolled_course_ids

    context = {
        'courses': courses
    }

    return render(request, 'student/home.html', context)

def student_enrollments_view(request):
    student_id = request.session.get('user_id')

    enrollments_response = api_request_with_refresh(
        request,
        'GET',
        f'http://127.0.0.1:8000/api/courses/enrollments/student/{student_id}/'
    )
    if isinstance(enrollments_response, HttpResponse):
        return enrollments_response

    if enrollments_response.status_code != 200:
        return HttpResponse("Failed to fetch enrollments")

    enrollments = enrollments_response.json()
    enrolled_course_ids = [enr['course'] for enr in enrollments]

    # Now fetch details of each course
    courses_response = api_request_with_refresh(request, 'GET', 'http://127.0.0.1:8000/api/courses/courses/')
    if isinstance(courses_response, HttpResponse):
        return courses_response

    all_courses = courses_response.json()
    enrolled_courses = [c for c in all_courses if c['id'] in enrolled_course_ids]

    return render(request, 'student/enrollments.html', {'courses': enrolled_courses})

def student_course_files(request, course_id):
    student_id = request.session.get('user_id')

    # Step 1: Check if student is enrolled in this course
    enrollment_check_url = f"http://127.0.0.1:8000/api/courses/enrollments/student/{student_id}/"
    enrollments_response = api_request_with_refresh(request, 'GET', enrollment_check_url)
    
    if isinstance(enrollments_response, HttpResponse):
        return enrollments_response  # Either 401 or redirect
    
    if enrollments_response.status_code != 200:
        return HttpResponse("Failed to fetch enrollments")

    enrollments = enrollments_response.json()
    enrolled_course_ids = {enrollment['course'] for enrollment in enrollments}

    if course_id not in enrolled_course_ids:
        return HttpResponseForbidden("You are not enrolled in this course.")

    # Step 2: Fetch course files using your custom endpoint
    course_files_url = f"http://127.0.0.1:8000/api/courses/CourseFiles/by-course/{course_id}/"
    files_response = api_request_with_refresh(request, 'GET', course_files_url)

    if isinstance(files_response, HttpResponse):
        return files_response
    
    if files_response.status_code != 200:
        return HttpResponse("Failed to fetch course files")

    files = files_response.json()

    # Step 3: Optionally get course title for heading
    course_info = next((e for e in enrollments if e['course'] == course_id), None)
    course_title = f"Course {course_id}"
    if course_info and 'course_title' in course_info:
        course_title = course_info['course_title']

    context = {
        'course_title': course_title,
        'files': files
    }

    return render(request, 'student/course_files.html', context)

def download_file(request,file_id):
    
    return FileResponse(file.file.open('rb'),as_attachment=True)