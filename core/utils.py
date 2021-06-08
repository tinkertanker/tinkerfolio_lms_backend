from core.models import Classroom
from rest_framework import status

def verify_classroom_owner(code, user):
    classroom = Classroom.objects.get(code=code)
    if classroom.teacher != user:
        return Response('This classroom does not belong to you.', status.HTTP_403_FORBIDDEN)
