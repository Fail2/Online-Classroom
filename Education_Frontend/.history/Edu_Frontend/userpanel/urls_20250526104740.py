from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [
    path('login/',views.user_login,name = 'user-login'),
    path('register/',views.user_register,name = 'user-register'),
    path('logout/', views.user_logout, name='user-logout'),
    path('teacher/home/',views.teacher_home,name = 'teacher-home'),
    path('teacher/add/courses/',views.add_course, name = 'add-course'),
    path('teacher/course/detail/<int: course_id>/',views.course_detail, name = 'course-detail'),
    path('teacher/edit/course/<int:course_id>',views.edit_course,name = 'edit-course'),
    path('teacher/delete/course/<int:course_id>',views.delete_course, name ='delete-course'),
    path('student/home/', views.student_home, name='student-home'),
]
