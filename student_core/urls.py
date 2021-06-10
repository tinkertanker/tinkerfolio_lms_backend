from django.urls import path, include
from rest_framework.routers import DefaultRouter
from student_core.views import *

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'initial', StudentInitialViewSet, basename="student_task_submission")

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]
