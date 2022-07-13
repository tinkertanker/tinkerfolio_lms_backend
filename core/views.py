import uuid
from itertools import chain
from rest_framework import viewsets
from rest_framework.response import Response
from django.core.files.base import ContentFile

from core.models import Classroom, Task, Submission, Announcement, ResourceSection, Resource
from accounts.models import User, StudentProfile
from core.serializers import *

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

    def delete(self, request, **kwargs):
        classroom = Classroom.objects.get(pk=int(kwargs['pk']))
        verify_classroom_owner(classroom.code, request.user)

        classroom.delete()

        return Response("classroom deleted")

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
        if 'display' in request.data:
            task.display = request.data['display']

        task.save()

        return Response(TaskSerializer(task).data)

    def update(self, request, **kwargs):
        task = Task.objects.get(pk=int(kwargs['pk']))

        verify_classroom_owner(task.classroom.code, request.user)

        task.name = request.data['name']
        task.description = request.data['description']
        task.status = request.data['status']
        task.max_stars = request.data['max_stars']
        if 'display' in request.data:
            task.display = request.data['display']
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

        if sub.stars != request.data['stars']: ## in case review accidentally submitted twice
            sub.stars = request.data['stars']
            sub.comments = request.data['comment']
            sub.save()

        return Response(SubmissionSerializer(sub).data)

class SubmissionStatusViewSet(viewsets.ViewSet):
    def list(self, request):
        ## All submission statuses from classroom
        tasks = Classroom.objects.get(code=request.query_params['code']).task_set.all()
        statuses_by_task = [task.submissionstatus_set.all() for task in tasks if task.submissionstatus_set.all()]
        statuses = [item for statuslist in statuses_by_task for item in statuslist]

        return Response(SubmissionStatusSerializer(statuses, many=True).data)

class AnnouncementViewSet(viewsets.ViewSet):
    def list(self, request):
        classroom = Classroom.objects.get(code=request.query_params['code'])
        announcements = Announcement.objects.filter(classroom=classroom)

        return Response(AnnouncementSerializer(announcements, many=True).data)

    def create(self, request):
        verify_classroom_owner(request.data['code'], request.user)

        announcement = Announcement(
            classroom=Classroom.objects.get(code=request.data['code']),
            name=request.data['name'],
            description=request.data['description'],
        )
        announcement.save()

        return Response(AnnouncementSerializer(announcement).data)

    def update(self, request, **kwargs):
        announcement = Announcement.objects.get(pk=int(kwargs['pk']))

        verify_classroom_owner(announcement.classroom.code, request.user)

        announcement.name = request.data['name']
        announcement.description = request.data['description']
        announcement.save()

        return Response(AnnouncementSerializer(announcement).data)

    def delete(self, request, **kwargs):
        announcement = Announcement.objects.get(pk=int(kwargs['pk']))

        verify_classroom_owner(announcement.classroom.code, request.user)

        announcement.delete()

        return Response("announcement deleted")

class ResourceSectionViewSet(viewsets.ViewSet):
    # def __init__(self, *args, **kwargs):
    #     file_fields = kwargs.pop('file_fields', None)
    #     super().__init__(*args, **kwargs)
    #     if file_fields:
    #         field_update_dict = {field: serializers.FileField(required=False, write_only=True) for field in file_fields}
    #         self.fields.update(**field_update_dict)

    def list(self, request):
        classroom = Classroom.objects.get(code=request.query_params['code'])
        sections = ResourceSection.objects.filter(classroom=classroom)
        resources = [{
            "section": ResourceSectionSerializer(section).data,
            "resources": ResourceSerializer(section.resource_set, many=True).data
        } for section in sections]

        return Response(resources)

    def create(self, request):
        classroom = Classroom.objects.get(code=request.data['code'])
        section = ResourceSection(classroom=classroom, name=request.data['name'])
        section.save()

        res_list = []
        for key, file in request.data.items():
            if 'file' in key:
                res = Resource(section=section, name=file.name)
                res.save()

                filename = 'res_{}_{}_{}'.format(
                    section.id, res.id, file.name
                )
                res.file.save(filename, ContentFile(file.read()))

                res_list.append(res)

        return Response({
            "section": ResourceSectionSerializer(section).data,
            "resources": ResourceSerializer(res_list, many=True).data
        })

    def destroy(self, request, **kwargs):
        rs = ResourceSection.objects.get(pk=int(kwargs['pk']))

        verify_classroom_owner(rs.classroom.code, request.user)

        rs.delete()

        return Response(True)

class ResourceViewSet(viewsets.ViewSet):
    def retrieve(self, request, **kwargs):
        resource = Resource.objects.get(id=kwargs['pk'])
        verify_classroom_owner(resource.section.classroom.code, request.user)
        return Response(ResourceSerializer(resource).data)

    def create(self, request):
        section = ResourceSection.objects.get(id=request.data['resource_section_id'])

        verify_classroom_owner(section.classroom.code, request.user)

        new_file = request.data['file']
        res = Resource(section=section, name=new_file.name)
        res.save()

        filename = 'res_{}_{}_{}'.format(
            section.id, res.id, new_file.name
        )
        res.file.save(filename, ContentFile(new_file.read()))

        return Response(ResourceSerializer(res).data)

    def destroy(self, request, **kwargs):
        res = Resource.objects.get(pk=int(kwargs['pk']))

        verify_classroom_owner(res.section.classroom.code, request.user)

        res.delete()

        return Response(True)
