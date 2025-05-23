from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated,SAFE_METHODS
from .models import Course,Enrollment,CourseFile
from .serializers import CourseSerializer,EnrollmentSerializer,CourseFileSerializer
from accounts.permissions import IsTeacher,IsStudent
from .permissions import IsCourseTeacher,IsEnrolledStudent
# Create your views here.

class CourseViewSet(viewsets.ModelViewSet):
    queryset =Course.objects.all()
    serializer_class = CourseSerializer

    def get_permissions(self):
        if self.action in ['partial_update','update','destroy']:
            return [IsCourseTeacher()]  # 👈 Instantiating the permission
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

    def get_permissions(self):
        if self.request.method in SAFE_METHODS: 
            # GET, HEAD,OPTIONS - for students
            return [IsAuthenticated(), IsEnrolledStudent]
        else:
            # POST,PUT,DELETE -for teachers
            return [IsAuthenticated(), IsCourseTeacher()]
        
    def get_queryset(self):
        user = self.request.user
        if user.role == 'TEACHER':
            #show only teacher's course file
            #SELECT * FROM course_file JOIN course ON course_file.course_id = course.id WHERE course.teacher_id = {user.id};
            return CourseFile.objects.filter(course__teacher=user)
        elif user.role == 'STUDENT':
            #show only course files of enrolled courses
            # SELECT cf.* FROM course_file cf JOIN course c ON cf.course_id = c.id JOIN enrollment e  ON e.course_id  = c.id WHERE e.student_id = {user.id};
            return CourseFile.objects.filter(course__enrollment__student= user)
        else: return CourseFile.object.none() #no access for others


