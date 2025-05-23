import os
from django.db import models

from accounts.models import User
# Create your models here.


def teacher_upload_path(instance,filename):
    return f"teacher_{instance.course.teacher.id}/course_{instance.course.id}/{filename}"
class Course(models.Model):
    title = models.CharField(max_length=100)
    description =models.TextField()
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role':'TEACHER'})
    created_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.title

class CourseFile(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='files')
    title =models.CharField(max_length=150)
    file =models.FileField(upload_to=teacher_upload_path)
    uploaded_at =models.DateTimeField(auto_now_add=True)   

    def __str__(self):
        return os.path.basename(self.file.name)

class Enrollment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role':'STUDENT'})
    course = models.ForeignKey(Course, on_delete=models.CASCADE)  
    enrolled_at = models.DateTimeField(auto_now_add = True) 

    class Meta: 
        constraints =[
            models.UniqueConstraint(fields=['student','course'],name='unique_enrollment')
        ]
