from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    ROLE_CHOICES =[
        ('ADMIN','Admin'),
        ('TEACHER','Teacher'),
        ('STUDENT','Student'),
    ]
    role = models.CharField(max_length=7,choices=ROLE_CHOICES,default='STUDENT')
    def __str__(self):
        return f"{self.username} ({self.role})"
