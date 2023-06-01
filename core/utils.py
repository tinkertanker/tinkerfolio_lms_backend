from core.models import Classroom
from student_core.models import Enroll
from rest_framework import status
from rest_framework.response import Response

def verify_classroom_owner(code, user):
    classroom = Classroom.objects.get(code=code)
    if classroom.teacher != user:
        return Response('This classroom does not belong to you.', status.HTTP_403_FORBIDDEN)

def verify_classroom_participant(code, user):
    # returns True if there is an entry with the classroom code and user, else False
    enroll = Enroll.objects.filter(classroom=code, studentUserID=user).exists()

    # no matching entry in the enrolls table -> student is not part of classroom
    if not enroll:
        return Response('You are not a student in this classroom.', status.HTTP_403_FORBIDDEN)
