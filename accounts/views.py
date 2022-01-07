from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from accounts.models import User, StudentProfile
from core.models import Classroom

class StudentRegister(viewsets.ViewSet):
    permission_classes = [AllowAny]

    def create(self, request):
        classroom = Classroom.objects.get(code=request.data['code'])
        new_index = max(classroom.student_indexes) + 1
        classroom.student_indexes = classroom.student_indexes + [new_index]
        classroom.save()

        student = User(username=request.data['code']+'_'+str(new_index), user_type=1)
        student.set_password(str(new_index))
        student.save()

        student_profile = StudentProfile(
            student=student, assigned_class_code=request.data['code'], index=new_index,
            created_by_student=True,
            name=request.data['name']
        )
        student_profile.save()

        return Response({'code': request.data['code'], 'index': new_index})
