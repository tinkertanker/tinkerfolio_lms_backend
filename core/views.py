import uuid
from rest_framework import viewsets
from core.models import Classroom
from accounts.models import User, StudentProfile
from core.serializers import ClassroomSerializer
from rest_framework.response import Response

class ClassroomViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = Classroom.objects.filter(teacher=request.user)
        classrooms = ClassroomSerializer(queryset, many=True)
        return Response(classrooms.data)

    def create(self, request):
        code = uuid.uuid4().hex[:6]

        ## Create classroom
        classroom = Classroom(
            teacher=request.user, code=code,
            name=request.data['name'], student_indexes=[i+1 for i in range(request.data['no_of_students'])]
        )
        classroom.save()

        for i in range(request.data['no_of_students']):
            ## Create User and StudentProfile for each student
            student = User(username=code+'_'+str(i+1))
            student.set_password(str(i+1))
            student.save()

            student_profile = StudentProfile(student=student, assigned_class_code=code, index=i+1)
            student_profile.save()

        return Response(ClassroomSerializer(classroom).data)

    def update(self, request, *args, **kwargs):
        classroom = Classroom.objects.get(pk=int(kwargs['pk']))

        classroom.name = request.data['name']
        classroom.status = request.data['status']

        indexes_to_remove = list(set(classroom.student_indexes) - set(request.data['student_indexes']))
        for index in indexes_to_remove:
            sp = StudentProfile.objects.get(assigned_class_code=classroom.code, index=index)
            sp.student.delete()

        indexes_to_add = list(set(request.data['student_indexes']) - set(classroom.student_indexes))
        for index in indexes_to_add:
            student = User(username=classroom.code+'_'+str(index))
            student.set_password(str(index))
            student.save()

            student_profile = StudentProfile(student=student, assigned_class_code=classroom.code, index=index)
            student_profile.save()

        classroom.student_indexes = request.data['student_indexes']
        classroom.save()

        return Response(ClassroomSerializer(classroom).data)
