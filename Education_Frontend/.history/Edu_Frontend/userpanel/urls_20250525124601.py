from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [
    path('login/',views.admin_login,name = 'admin-login'),
    path('register/',views.admin_register,name = 'admin-register'),
    path('dashboard/', views.admin_dashboard, name='admin-dashboard'),
    path('teachers/', views.teacher_list, name='teacher-list'),
    path('students/', views.student_list, name='student-list'),
    path('courses/', views.course_list, name='course-list'),
    path('logout/', views.admin_logout, name='admin-logout'),
]
