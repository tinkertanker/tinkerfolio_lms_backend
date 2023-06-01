import uuid
from rest_framework.decorators import api_view
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from django.core.files.base import ContentFile

from core.models import Classroom, Task
from accounts.models import User, StudentProfile
from student_core.models import Enroll
from core.serializers import *

from datetime import datetime

from core.utils import verify_classroom_participant

class StudentInitialViewSet(viewsets.ViewSet):
    def list(self, request):
        ## Get student's initial tasks and submissions
        if request.user.user_type != 1:
            return Response('User is not a student.', status.HTTP_403_FORBIDDEN)

        profile = StudentProfile.objects.get(student=request.user)
        classroom = Classroom.objects.get(code=profile.assigned_class_code)
        announcements_queryset = classroom.announcement_set.all()

        sections = ResourceSection.objects.filter(classroom=classroom)
        resources = [{
            "section": ResourceSectionSerializer(section).data,
            "resources": ResourceSerializer(section.resource_set, many=True).data
        } for section in sections]

        task_queryset = classroom.task_set.filter(display=1)
        submission_statuses_queryset = [task.submissionstatus_set.filter(student=request.user).first() for task in task_queryset]
        submissions_queryset = [task.submission_set.filter(student=request.user).first() for task in task_queryset]

        return Response({
            'profile': StudentProfileSerializer(profile).data,
            'classroom': ClassroomSerializer(classroom).data,

            'announcements': AnnouncementSerializer(announcements_queryset, many=True).data,
            'resources': resources,

            'tasks': TaskSerializer(task_queryset, many=True).data,
            'submission_statuses': [SubmissionStatusSerializer(substatus).data for substatus in submission_statuses_queryset if substatus != None],
            'submissions': [SubmissionSerializer(sub).data for sub in submissions_queryset if sub != None]
        })

class StudentSubmissionViewSet(viewsets.ViewSet):
    def retrieve(self, request, **kwargs):
        sub = Submission.objects.get(id=int(kwargs['pk']))
        if request.user != sub.student:
            return Response('Submission does not belong to student.', status.HTTP_403_FORBIDDEN)

        return Response(SubmissionSerializer(sub).data)

    def create(self, request):
        if request.user.user_type != 1:
            return Response('User is not a student.', status.HTTP_403_FORBIDDEN)

        sub = Submission(task=Task.objects.get(id=request.data['task_id']), student=request.user)

        if 'text' in request.data:
            sub.text = request.data['text']

        if 'image' in request.data:
            image = request.data['image']
            filename = '{}_{}_{}.{}'.format(
                request.user.studentprofile.assigned_class_code, request.data['task_id'],
                request.user.id, image.name.split('.')[1]
            )
            sub.image.save(filename, ContentFile(image.read()))

        sub.save()

        return Response(SubmissionSerializer(sub).data)

    def update(self, request, **kwargs):
        if request.user.user_type != 1:
            return Response('User is not a student.', status.HTTP_403_FORBIDDEN)

        sub = Submission.objects.get(id=int(kwargs['pk']))

        if sub.stars or sub.comments:
            return Response('Submission has already been graded.', status.HTTP_403_FORBIDDEN)

        if 'text' in request.data:
            sub.text = request.data['text']

        if 'image' in request.data:
            image = request.data['image']
            filename = '{}_{}_{}.{}'.format(
                request.user.studentprofile.assigned_class_code, request.data['task_id'],
                request.user.id, image.name.split('.')[1]
            )
            sub.image.save(filename, ContentFile(image.read()))

        sub.resubmitted_at = datetime.now()
        sub.save()

        return Response(SubmissionSerializer(sub).data)

class MyUserPermissions(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):

        # Allow get requests for all
        if request.method == 'GET':
            return True
        return request.user == obj

# class StudentSubmissionStatusViewSet(viewsets.ModelViewSet):
#     """
#     A viewset for viewing and editing user instances.
#     """
#     serializer_class = SubmissionStatusSerializer
#     queryset = SubmissionStatus.objects.all()
#     permission_classes = (MyUserPermissions, )

class StudentSubmissionStatusViewSet(viewsets.ViewSet):

    def create(self, request):
        substatus = SubmissionStatus(
            task=Task.objects.get(id=request.data['task_id']),
            student=request.user, status=request.data['status']
        )
        substatus.save()

        return Response(SubmissionStatusSerializer(substatus).data)

    def update(self, request, **kwargs):
        status = SubmissionStatus.objects.get(pk=int(kwargs['pk']))

        status.status = request.data['status']
        status.save()

        return Response(SubmissionStatusSerializer(status).data)

class StudentResourceViewSet(viewsets.ViewSet):
    def retrieve(self, request, **kwargs):
        resource = Resource.objects.get(id=kwargs['pk'])
        if request.user.studentprofile.assigned_class_code != resource.section.classroom.code:
            return Response('Student not part of this classroom.', status.HTTP_403_FORBIDDEN)
        return Response(ResourceSerializer(resource).data)
    
class EnrollViewSet(viewsets.ViewSet):
    # need to retrieve and list all classrooms the student is in
    def list(self, request):
        # Obtains a list of all the Classrooms belonging to the teacher, with all the attributes

        queryset = Classroom.objects.filter(studentUserID=request.user)
        classrooms = ClassroomSerializer(queryset, many=True)
        return Response(classrooms.data)

    def retrieve(self, request, **kwargs):
        if request.user.user_type == 2:
            return Response('User is not a student.', status.HTTP_403_FORBIDDEN)
        
        verify_classroom_participant(kwargs['pk'], request.user)
        classroom = Classroom.objects.get(code=kwargs['pk'])
        return Response(ClassroomSerializer(classroom).data)


@api_view(['GET'])
def Leaderboard(request):
    profile_instances = StudentProfile.objects.filter(assigned_class_code=request.user.studentprofile.assigned_class_code)
    profiles = StudentProfileSerializer(profile_instances, many=True).data
    return Response(profiles)
