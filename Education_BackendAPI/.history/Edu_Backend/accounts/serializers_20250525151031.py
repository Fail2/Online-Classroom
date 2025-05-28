from rest_framework import serializers
from .models import User

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','email','password','role']
        extra_kwargs = {'password':{'write_only':True}}

    def create(self,validated_data):
        user = User.objects.create_user(**validated_data) # hashed password because of create_user
        return user    
    
class CustomTokenObtainPairSerializers(TokenObtainPairSerializer):
    def validate(self,attrs):
        data = super().validate(attrs)
        # Add custom user info to response
        data['user'] ={
            'id':self.user.id,
            'username':self.user.username,
            'email': self.user.email,
            'role':self.user.role,
        }   
        return data 

