from rest_framework import serializers
from .models import User

# User creation serializer
class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username','password', 'email', 'first_name', 'last_name','user_type' )
        extra_kwargs = {'password':{'write_only':True}}

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        user.set_password(validated_data['password'])
        user.save()
        return user

# User login Serializer
class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


# Logout Serializer
class UserLogoutSerializer(serializers.Serializer):
    pass

