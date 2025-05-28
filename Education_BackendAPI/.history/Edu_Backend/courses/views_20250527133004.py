from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated,SAFE_METHODS
from .models import Course,Enrollment,CourseFile
from .serializers import CourseSerializer,EnrollmentSerializer,CourseFileSerializer
from accounts.permissions import IsTeacher,IsStudent,IsAdmin
from .permissions import IsCourseTeacher,IsEnrolledStudent
from rest_framework.response import Response
from rest_framework.decorators import action
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
            return [IsEnrolledStudent() if self.request.user.role == 'STUDENT' else IsCourseTeacher()]
        return []


class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'TEACHER':
            return Enrollment.objects.filter(course__teacher=user)
        elif user.role == 'STUDENT':
            return Enrollment.objects.filter(student=user)
        return Enrollment.objects.none()

    def get_permissions(self):
        if self.action == 'create':
            return [IsStudent()]
        elif self.action in ['update', 'destroy', 'retrieve']:
            if self.request.user.role == 'STUDENT':
                return [IsEnrolledStudent()]
            elif self.request.user.role == 'TEACHER':
                return [IsTeacher()]
        return []

    @action(detail=False, methods=['get'], url_path='student/(?P<student_id>[^/.]+)')
    def student_enrollments(self, request, student_id=None):
        # Ensure students can only access their own enrollments
        if request.user.role != 'STUDENT' or request.user.id != int(student_id):
            return Response({'error': 'Unauthorized'}, status=403)

        enrollments = Enrollment.objects.filter(student_id=student_id)
        serializer = self.get_serializer(enrollments, many=True)
        return Response(serializer.data)
    
class CourseFileViewSet(viewsets.ModelViewSet):
    serializer_class = CourseFileSerializer

    def get_permissions(self):
        if self.request.method in SAFE_METHODS: 
            # GET, HEAD,OPTIONS - for students
            if self.request.user.role == 'STUDENT':
                return [IsAuthenticated(), IsEnrolledStudent()]
            else:
                return [IsAuthenticated(),IsCourseTeacher()]
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

    @action(detail = False, methods=['get'],url_path='by_course/?p<course_id>[^/.]+') 
    def by_course(self, request, course_id = None):
        user = request.user

        try:
            course = Course.objects.get(id = course_id)
        except Course.DoesNotExist:
            return Response({'error':'Course not found'},status =404)

        # Apply permission classes manually       
        if user.role == 'STUDENT':
            if not course.enrollment_set.filter(student = user).exists():
                return Response({'error':'You are not enrolled in this course'},status =403)
        elif user.role == 'TEACHER':
            if not course.teacher != user:
                return Response({'error':'You do not teach this course.'},status=403)    
        files = CourseFile.objects.filter(course = course)
        serializer = self.get_serializer(files, many = True)
        return Response(serializer.data)        
