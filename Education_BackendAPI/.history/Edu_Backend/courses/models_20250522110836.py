from django.db import models
from accounts.models import User
# Create your models here.

class Course(models.Model):
    title = models.CharField(max_length=100)
    description =models.TextField()