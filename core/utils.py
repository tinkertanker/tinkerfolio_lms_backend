from core.models import Classroom
from rest_framework import status
from rest_framework.response import Response

def verify_classroom_owner(code, user):
    classroom = Classroom.objects.get(code=code)
    if classroom.teacher != user:
        return Response('This classroom does not belong to you.', status.HTTP_403_FORBIDDEN)
