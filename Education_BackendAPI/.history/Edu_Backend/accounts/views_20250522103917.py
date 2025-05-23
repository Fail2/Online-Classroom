from django.shortcuts import render
from rest_framework import viewsets
from .models import User
from .serializers import UserSerializer
from .permissions import IsAdmin
# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin] #only admin can manage users