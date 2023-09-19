from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.tokens import Token
from .models import User
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny  # Import AllowAny permission
from .serializers import UserRegistrationSerializer, UserLoginSerializer
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework_jwt.settings import api_settings
from django.contrib.auth import authenticate
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import AllowAny



jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

# Create your views

# User Registration to api
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [AllowAny]  # By default, only authenticated users can perform actions

    # Example API endpoint to create a new user
    def create(self, request, *args, **kwargs):
        # Allow unauthenticated users to create (sign up) a new user
        self.permission_classes = [AllowAny]

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Example API endpoint to update an existing user
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.serializer_class(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# User Login View to api

@authentication_classes([])  # Specify an empty list of authentication classes
@permission_classes([AllowAny])  # Specify that any user (authenticated or not) is allowed
class UserLoginView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.user_type == 'employee':
                    request.session['user_type'] = 'employee'
                else:
                    request.session['user_type'] = 'guest'

                # User is authenticated, generate a token
                # payload = jwt_payload_handler(user)
                # token = jwt_encode_handler(payload)
                response_data = {
                    'token': token,
                    'user_id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'expires_at': payload['exp'],  # Include token expiration time
                    
                }
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Logout View
# @authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
class UserLogoutView(APIView):
    def post(self, request):
        
        if 'user_type' in request.session:
            del request.session['user_type']
        # try:
        refresh_token = request.data.get('refresh_token')
        token = RefreshToken(refresh_token)
        print("Token is : " , token)
        # token.blacklist()
            # jwt_payload = api_settings.JWT_PAYLOAD_GETTER(request.user)
            # jwt_payload['exp'] = 0
            # token = api_settings.JWT_ENCODE_HANDLER(jwt_payload)
        return Response({'detail': 'User logged out successfully.'}, status=status.HTTP_200_OK)
        # except Exception as e:
        #     return Response(status=status.HTTP_400_BAD_REQUEST)

    

class HomeView(APIView):
     
    permission_classes = (IsAuthenticated, )
    def get(self, request):
        content = {'message': 'Welcome to the JWT Authentication page using React Js and Django!'}
        return Response(content)    


def index_view(request):
    return render(request, 'build/index.html')