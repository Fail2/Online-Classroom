from rest_framework.permissions import BasePermission
from .models import Course

class IsCourseTeacher(BasePermission):
    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'teacher'):  # obj is a Course
            return request.user == obj.teacher
        elif hasattr(obj, 'course') and hasattr(obj.course, 'teacher'):  # obj is a CourseFile
            return request.user == obj.course.teacher
        return False
    
class IsEnrolledStudent(BasePermission):
    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Course):
            return obj.enrollment_set.filter(student=request.user).exists()
        elif hasattr(obj, 'course') and isinstance(obj.course, Course):
            return obj.course.enrollment_set.filter(student=request.user).exists()
        return False

