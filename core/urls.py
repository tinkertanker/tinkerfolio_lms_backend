from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core.views import *

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'classrooms', ClassroomViewSet, basename="classroom")
router.register(r'student_profiles', StudentProfileViewSet, basename="student_profile")
router.register(r'tasks', TaskViewSet, basename="task")
router.register(r'submissions', SubmissionViewSet, basename="submission")
router.register(r'submission_status', SubmissionStatusViewSet, basename="submission_status")
router.register(r'announcements', AnnouncementViewSet, basename="announcement")
router.register(r'resource_section', ResourceSectionViewSet, basename="resource_section")
router.register(r'resource', ResourceViewSet, basename="resource")
router.register(r'student_list', StudentViewSet, basename="student_list"),
# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]
