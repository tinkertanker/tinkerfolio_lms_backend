from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView, 
)
from .views import StudentRegister, TeacherSignUp, StudentSignUp, CustomTokenObtainPairView, CustomTokenVerifyView, CustomTokenRefreshView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'student_register', StudentRegister, basename="student_register")

# USE THIS FOR SIGN UP
router.register(r'teacher_signup', TeacherSignUp, basename="teacher_signup")
router.register(r'student_signup', StudentSignUp, basename="student_signup")

urlpatterns = [
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', CustomTokenVerifyView.as_view(), name='token_verify'),
    path('token/', include(router.urls)),
]
