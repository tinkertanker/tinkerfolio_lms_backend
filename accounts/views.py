from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed

from accounts.models import User, StudentProfile
from core.models import Classroom
from student_core.models import Enroll

class TeacherSignUp(viewsets.ViewSet):
    permission_classes = [AllowAny]
    def create(self, request):

        if User.objects.filter(username=request.data['username']).exists():
            return Response({'error': 'Username already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=request.data['email']).exists():
            return Response({'error': 'Email already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        teacher = User(username=request.data['username'], user_type=2, email=request.data['email'], first_name=request.data['first_name'])
        teacher.set_password(request.data['password'])

        teacher.save()

        return Response({'Account': 'Teacher','Username': request.data['username'], 'First Name': request.data['first_name']})


class StudentSignUp(viewsets.ViewSet):
    permission_classes = [AllowAny]
    def create(self, request):

        if User.objects.filter(username=request.data['username']).exists():
            return Response({'error': 'Username already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=request.data['email']).exists():
            return Response({'error': 'Email already exists.'}, status=status.HTTP_400_BAD_REQUEST)
        
        student = User(username=request.data['username'], user_type=1, email=request.data['email'], first_name=request.data['first_name'])
        student.set_password(request.data['password'])
        
        student.save()

        return Response({'Account': 'Student','Username': 'username', 'First Name': 'first_name'})

class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.user
        inputUserType = request.data.get('userType')
        inputUserCode = 0
        if inputUserType == "teacher":
            inputUserCode = 2
        elif inputUserType == "student":
            inputUserCode = 1
        if user.user_type != inputUserCode:
            raise AuthenticationFailed('Invalid user type.')

        tokens = serializer.validated_data
        response_data = {
            'access': str(tokens['access']),
            'refresh': str(tokens['refresh']),
            'userType': user.user_type,
        }

        print(response_data)

        return Response(response_data)

class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
      

        tokens = serializer.validated_data
        response_data = {
            'access': str(tokens['access']),
            # 'refresh': str(tokens['refresh']),
        }

        print(response_data)

        return Response(response_data)

class CustomTokenVerifyView(TokenVerifyView):
    pass
