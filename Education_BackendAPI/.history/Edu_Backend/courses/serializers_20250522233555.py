from rest_framework import serializers
from .models import Course,Enrollment
from django.core.exceptions import ValidationError

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = '__all__'

    def clean(self):
        #Check if student already has 5 active enrollments
        if self.student.role=='STUDENT':
            active_enrollments = Enrollment.objects.filter(student = self.student).count() 
            if active_enrollments>=5:
                raise ValidationError("students cannot enroll in more than 5 courses.")
    def save(self,*args,**kwargs):
        self.full_clean # Runs clean() before saving
        super().save(*args, **kwargs)        