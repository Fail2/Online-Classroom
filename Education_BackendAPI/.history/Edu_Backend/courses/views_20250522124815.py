from django.shortcuts import render
from rest_framework import viewsets
from .models import Course,Enrollment
from .serializers import CourseSerializer,EnrollmentSerializer
from accounts.permissions import IsTeacher,IsStudent
# Create your views here.

class CourseViewSet(viewsets.ModelViewSet):
    queryset =Course.objects.all()
    serializer_class = CourseSerializer
    