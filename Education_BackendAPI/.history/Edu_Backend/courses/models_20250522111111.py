from django.db import models
from accounts.models import User
# Create your models here.

class Course(models.Model):
    title = models.CharField(max_length=100)
    description =models.TextField()
    teacher = models.ForeignKey(User,on_delete=models.CASCADE,limit_choices_to={'role':'TEACHER'})
    created_at = models.DateTimeField(auto_now_add = True)