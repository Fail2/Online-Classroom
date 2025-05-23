from django.shortcuts import render
from rest_framework import viewsets
from .models import Course,Enrollment
from .serializers import CourseSerializer,EnrollmentSerializer,CourseFileSerializer
from accounts.permissions import IsTeacher,IsStudent
from .permissions import IsCourseTeacher,IsEnrolledStudent
# Create your views here.

class CourseViewSet(viewsets.ModelViewSet):
    queryset =Course.objects.all()
    serializer_class = CourseSerializer

    def get_permissions(self):
        if self.action in ['partial_update','update','destroy']:
            return [IsCourseTeacher()]
        elif self.action =='create':
            return [IsTeacher()]
        elif self.action == 'retrieve':
            return [IsEnrolledStudent]
        return []


class EnrollmentViewSet(viewsets.ModelViewSet):
    serializer_class = EnrollmentSerializer

    def get_queryset(self):
        if self.request.user.role == 'TEACHER':
            return Enrollment.objects.filter(course__teacher = self.request.user)    
        return Enrollment.objects.filter(student = self.request.user)
    def get_permissions(self):
        if self.action in ['create']:
            return [IsStudent()]
        elif self.action in ['update', 'destroy', 'retrieve']:
            return [IsTeacher(), IsEnrolledStudent()] 
        return []
    
class CourseFileViewSet(viewsets.ModelViewSet):
    serializer_class = CourseFileSerializer    


