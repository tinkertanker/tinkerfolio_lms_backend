from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core.views import *

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'classrooms', ClassroomViewSet, basename="classroom")
router.register(r'student_profiles', StudentProfileViewSet, basename="student_profile")

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]
