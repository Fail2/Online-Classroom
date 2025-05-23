from rest_framework import serializers
from .models import Course,Enrollment,CourseFile
from django.core.exceptions import ValidationError

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = '__all__'

    def validate(self, data):
        student = data['student']
        if student.role != 'STUDENT':
            raise serializers.ValidationError("Only students can enroll in courses.")
        
        # Check existing enrollments
        if Enrollment.objects.filter(student=student).count() >= 5:
            raise serializers.ValidationError("Maximum 5 course enrollments allowed.")
        
        return data    
class CourseFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseFile
        fields = '__all__'
        read_only_fields = ['uploaded_at']

    def validate(self, value):
        if self.context['request'].user!= value.teacher:
            raise serializers.ValidationError("You can only add files to your own courses")
        return value   

