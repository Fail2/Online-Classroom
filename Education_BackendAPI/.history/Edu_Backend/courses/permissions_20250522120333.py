from rest_framework.permissions import BasePermission
from .models import Course

class IsCourseTeacher(BasePermission):
    def has_permission(self, request, view,obj):
        return request.user == obj.teacher