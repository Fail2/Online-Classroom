from rest_framework.permissions import BasePermission
from .models import Course

class IsCourseTeacher(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.teacher
    
class IsEnrolledStudent(BasePermission):
    def has_object_permission(self, request, view,obj):
        return obj.enrollment_set.filter(student=request.user).exists()#in this obj = specific course for this we are using reverse manager