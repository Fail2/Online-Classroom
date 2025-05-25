from django.shortcuts import render
from rest_framework import viewsets
from .models import User
from .serializers import UserSerializer,CustomTokenObtainPairSerializers
from .permissions import IsAdmin
from rest_framework_simplejwt.views import TokenObtainPairView
# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    #permission_classes = [IsAdmin] #only admin can manage users # 👈 Passing the class itself (not calling it)

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializers    