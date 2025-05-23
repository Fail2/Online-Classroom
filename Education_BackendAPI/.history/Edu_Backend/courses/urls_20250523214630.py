from django.contrib import admin
from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet,EnrollmentViewSet,CourseFileViewSet

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='course')
router.register(r'enrollments', EnrollmentViewSet, basename='enrollment')
router.register(r'CourseFiles', CourseFileViewSet, basename='coursefile')
urlpatterns = [
    path('',include(router.urls)),
]
