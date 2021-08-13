import uuid
from itertools import chain
from rest_framework import viewsets
from rest_framework.response import Response

from core.models import Classroom, Task, Submission
from accounts.models import User, StudentProfile
from core.serializers import ClassroomSerializer, StudentProfileSerializer, TaskSerializer, SubmissionSerializer

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
            student = User(username=code+'_'+str(i+1), user_type=1)
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

        print(request.data)

        indexes_to_remove = list(set(classroom.student_indexes) - set(request.data['student_indexes']))
        for index in indexes_to_remove:
            sp = StudentProfile.objects.get(assigned_class_code=classroom.code, index=index)
            sp.student.delete()

        indexes_to_add = list(set(request.data['student_indexes']) - set(classroom.student_indexes))
        print('indexes to add:', indexes_to_add)
        for index in indexes_to_add:
            student = User(username=classroom.code+'_'+str(index), user_type=1)
            student.set_password(str(index))
            student.save()

            try:
                student_name = [newName['name'] for newName in request.data['newNames'] if newName['index'] == index][0]
            except:
                student_name = ""

            student_profile = StudentProfile(
                student=student, assigned_class_code=classroom.code, index=index,
                name=student_name
            )
            student_profile.save()

        classroom.student_indexes = request.data['student_indexes']
        classroom.save()

        return Response(ClassroomSerializer(classroom).data)

class StudentProfileViewSet(viewsets.ViewSet):
    def list(self, request):
        ## student ID is from User instance, not StudentProfile instance
        verify_classroom_owner(request.query_params['code'], request.user)

        queryset = StudentProfile.objects.filter(assigned_class_code=request.query_params['code'])
        profiles = []
        for sp in queryset:
            profile = StudentProfileSerializer(sp).data
            profile['id'] = sp.student.id
            profiles.append(profile)
        return Response(profiles)

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

class SubmissionViewSet(viewsets.ViewSet):
    def list(self, request):
        ## All submissions from classroom
        tasks = Classroom.objects.get(code=request.query_params['code']).task_set.all()
        subs_by_task = [task.submission_set.all() for task in tasks if task.submission_set.all()]
        subs = [item for sublist in subs_by_task for item in sublist]

        return Response(SubmissionSerializer(subs, many=True).data)

    def update(self, request, **kwargs):
        sub = Submission.objects.get(pk=int(kwargs['pk']))

        verify_classroom_owner(sub.task.classroom.code, request.user)

        sub.stars = request.data['stars']
        sub.comments = request.data['comment']
        sub.save()

        return Response(SubmissionSerializer(sub).data)
