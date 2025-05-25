from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [
    path('login/',views.user_login,name = 'user-login'),
    path('register/',views.user_register,name = 'user-register'),
    path('logout/', views.user_logout, name='user-logout'),
    ('teacher/home/',views.teacher-home,name = 'teacher-home'),
    path('student/home/', views.student-home, name='student-home'),
]
