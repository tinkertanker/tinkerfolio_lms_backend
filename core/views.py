import uuid
from rest_framework import viewsets
from rest_framework.response import Response

from core.models import Classroom, Task
from accounts.models import User, StudentProfile
from core.serializers import ClassroomSerializer, StudentProfileSerializer, TaskSerializer

from core.utils import verify_classroom_owner

class ClassroomViewSet(viewsets.ViewSet):

    def list(self, request):
        queryset = Classroom.objects.filter(teacher=request.user)
        classrooms = ClassroomSerializer(queryset, many=True)
        return Response(classrooms.data)

    def retrieve(self, request, **kwargs):
        ## Uses class code instead of pk
        verify_classroom_owner(kwargs['pk'], request.user)
        classroom = Classroom.objects.get(code=kwargs['pk'])
        return Response(ClassroomSerializer(classroom).data)

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

    def update(self, request, **kwargs):
        classroom = Classroom.objects.get(pk=int(kwargs['pk']))
        verify_classroom_owner(classroom.code, request.user)

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

class StudentProfileViewSet(viewsets.ViewSet):
    def list(self, request):
        verify_classroom_owner(request.query_params['code'], request.user)

        queryset = StudentProfile.objects.filter(assigned_class_code=request.query_params['code'])
        profile = StudentProfileSerializer(queryset, many=True)
        return Response(profile.data)

    def update(self, request, **kwargs):
        verify_classroom_owner(request.data['code'], request.user)

        profile = StudentProfile.objects.get(assigned_class_code=request.data['code'], index=request.data['index'])
        profile.name = request.data['name']
        profile.save()
        return Response('done')

class TaskViewSet(viewsets.ViewSet):
    def list(self, request):
        verify_classroom_owner(request.query_params['code'], request.user)

        classroom = Classroom.objects.get(code=request.query_params['code'])
        queryset = Task.objects.filter(classroom=classroom)
        return Response(TaskSerializer(queryset, many=True).data)

    def create(self, request):
        print(request.data)
        verify_classroom_owner(request.data['code'], request.user)

        task = Task(
            classroom=Classroom.objects.get(code=request.data['code']),
            name=request.data['name'],
            description=request.data['description'],
            max_stars=request.data['max_stars']
        )
        task.save()

        return Response(TaskSerializer(task).data)

    def update(self, request, **kwargs):
        task = Task.objects.get(pk=int(kwargs['pk']))

        verify_classroom_owner(task.classroom.code, request.user)

        task.name = request.data['name']
        task.description = request.data['description']
        task.status = request.data['status']
        task.max_stars = request.data['max_stars']
        task.save()

        return Response(TaskSerializer(task).data)

    def delete(self, request, **kwargs):
        task = Task.objects.get(pk=int(kwargs['pk']))

        verify_classroom_owner(task.classroom.code, request.user)

        task.delete()

        return Response("task deleted")
