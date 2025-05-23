from django.shortcuts import render
from rest_framework import viewsets
from .models import Course,Enrollment
from .serializers import CourseSerializer,EnrollmentSerializer
from accounts.permissions import IsTeacher,IsStudent
# Create your views here.

class CourseViewSet(viewsets.ModelViewSet):
    queryset =Course.objects.all()
    serializer_class = CourseSerializer

    def get_permissions(self):
        if self.action in ['create','update','destroy']:
            return [IsTeacher()]
        return []    


class EnrollmentViewSet(viewsets.ModelViewSet):
    serializer_class = EnrollmentSerializer

    def get_queryset(self):
        if self.request.user.role == 'TEACHER':
            return Enrollment.objects.filter(course__teacher = self.request.user)    
        return Enro    