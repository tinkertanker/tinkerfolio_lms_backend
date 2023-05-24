from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from accounts.models import User, StudentProfile
from core.models import Classroom


class StudentRegister(viewsets.ViewSet):
    '''
    Allows a student to sign themselves up as a new student in the classroom
    '''
    permission_classes = [AllowAny]

    def create(self, request):
        # Obtains the classroom code, sets up the index number of the student and updates the classroom
        classroom = Classroom.objects.get(code=request.data['code'])
        new_index = max(classroom.student_indexes) + 1
        classroom.student_indexes = classroom.student_indexes + [new_index]
        classroom.save()

        # Creates a new user profile
        student = User(
            username=request.data['code']+'_'+str(new_index), user_type=1)
        student.set_password(str(new_index))
        student.save()

        # Sets up the student profile and saves it
        student_profile = StudentProfile(
            student=student, assigned_class_code=request.data['code'], index=new_index,
            created_by_student=True,
            name=request.data['name']
        )
        student_profile.save()

        return Response({'code': request.data['code'], 'index': new_index})

