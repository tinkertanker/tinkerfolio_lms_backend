import uuid
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status

from core.models import Classroom, Task
from accounts.models import User, StudentProfile
from core.serializers import *

class StudentInitialViewSet(viewsets.ViewSet):
    def list(self, request):
        ## Get student's initial tasks and submissions
        if request.user.user_type != 1:
            return Response('User is not a student.', status.HTTP_403_FORBIDDEN)

        profile = StudentProfile.objects.get(student=request.user)
        classroom = Classroom.objects.get(code=profile.assigned_class_code)
        task_queryset = classroom.task_set.all()
        submissions_queryset = [task.submission_set.filter(student=request.user).first() for task in task_queryset]

        return Response({
            'profile': StudentProfileSerializer(profile).data,
            'classroom': ClassroomSerializer(classroom).data,
            'tasks': TaskSerializer(task_queryset, many=True).data,
            'submissions': [SubmissionSerializer(sub).data for sub in submissions_queryset if sub != None]
        })
