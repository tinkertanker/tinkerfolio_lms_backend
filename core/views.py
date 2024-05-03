import uuid
from itertools import chain
from django.utils import timezone

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.core.files.base import ContentFile

from core.models import Classroom, Task, Submission, Announcement, ResourceSection, Resource
from accounts.models import User
from core.serializers import *

from core.utils import verify_classroom_owner

import random
class ClassroomViewSet(viewsets.ViewSet):
    '''
    Relates to classroom management, accessible only by teachers and admins, and has 5 methods:
    1. List - obtains a list of all classrooms assigned to the teacher
    2. Retrieve - obtains details about a specific classroom assigned to the teacher
    3. Create - creates a new classroom, 
    4. Update - updates class details, such as the name, status, and the number of students in the class
    5. Delete - deletes a class
    '''

    def list(self, request):
        # Obtains a list of all the Classrooms belonging to the teacher, with all the attributes
        queryset = Classroom.objects.filter(teacher=request.user)
        classrooms = ClassroomSerializer(queryset, many=True)
        return Response(classrooms.data)

    def retrieve(self, request, **kwargs):
        # Uses class code instead of pk
        verify_classroom_owner(kwargs['pk'], request.user)
        classroom = Classroom.objects.get(code=kwargs['pk'])
        return Response(ClassroomSerializer(classroom).data)

    def create(self, request):
        print(request.data)
        # Creates a new classroom code
        code = uuid.uuid4().hex[:6]

        classroom = Classroom(
        teacher=request.user, code=code,
        name=request.data['name'], 
        student_indexes=[], 
        )
        
        classroom.save()

        return Response(ClassroomSerializer(classroom).data)

    def update(self, request, **kwargs):
        '''
        Allows the teacher to update at least one of the following three things:
            1. Update class name
            2. Update class status
            3. Update number of students in the class - either remove or add new students
        '''

        # Obtains classrom based on the ID, and verifies teacher
        classroom = Classroom.objects.get(pk=int(kwargs['pk']))
        verify_classroom_owner(classroom.code, request.user)

        classroom.name = request.data['name']
        classroom.status = request.data['status']

        print(request.data)

        # Finds the indexes of students to remove and deletes them from the class
        indexes_to_remove = list(
            set(classroom.student_indexes) - set(request.data['student_indexes']))
        for index in indexes_to_remove:
            sp = Enroll.objects.get(studentIndex=index, classroom=classroom)
            sp.delete()

        # Finds the number of indexes to add and automatically creates users
        indexes_to_add = list(
            set(request.data['student_indexes']) - set(classroom.student_indexes))
        print('indexes to add:', indexes_to_add)
        for index in indexes_to_add:
            # Automatically creates a user account based on classcode and index
            student = User(username=classroom.code+'_'+str(index), user_type=1)
            student.set_password(str(index))
            student.save()

            try:
                # Tries to obtain the student name from input based on the index. If no name is found, name is set to empty str
                student_name = [
                    newName['name'] for newName in request.data['newNames'] if newName['index'] == index][0]
            except:
                student_name = ""

            student_profile = Enroll(studentUserID=student, studentIndex=index, classroom=classroom, name=student_name)
            student_profile.save()

        classroom.student_indexes = request.data['student_indexes']
        classroom.save()

        return Response(ClassroomSerializer(classroom).data)

    def delete(self, request, **kwargs):
        # Allows teacher to delete the classroom
        classroom = Classroom.objects.get(pk=int(kwargs['pk']))
        verify_classroom_owner(classroom.code, request.user)

        classroom.delete()

        return Response("classroom deleted")

@api_view(['POST'])
def BulkView(request, **kwargs):
    class_code = request.query_params['code']
    classroom = Classroom.objects.get(code=class_code)
    
    prefix = request.query_params['prefix']
    if prefix == "": prefix = classroom.name
    
    raw_names = request.query_params['names'].split("\n")
    names = list(filter(lambda x : x != "", raw_names))
    names_idx = 0
    
    number_students = int(request.query_params['number'])
    number_students = max(len(names), number_students)
    suffix = 0
    
    new_students = []
    all_names = list(User.objects.values_list("username", flat=True))
    for i in range(number_students):
        suffix += 1
        new_username = prefix+str(suffix)
        while new_username in all_names:
            suffix += 1
            new_username = prefix+str(suffix)
        
        password_length = 10
        new_password = "".join([random.SystemRandom().choice("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%^&*()") for i in range(password_length)])
        print("Adding user")
        print(new_username, new_password)

        if names_idx < len(names):
            new_name = names[names_idx]
            names_idx += 1
        else:
            new_name = "Student "+str(suffix)

        #create the new account
        student = User(username=new_username, user_type=1, email=new_username+"@tinkerfolio.com", first_name=new_name)
        student.set_password(new_password)
        student.save()
        
        #enroll the new account using the class code
        present_students = Enroll.objects.filter(classroom=classroom)
        num_of_students = len(present_students)
        new_index = present_students[present_students.count()-1].studentIndex+1
        classroom.student_indexes = classroom.student_indexes + [new_index]
        classroom.save()
        
        enroll = Enroll(classroom=classroom, studentUserID=student, studentIndex=new_index, score=0)
        enroll.save()
        print(enroll)

        new_students.append({"username": new_username, "password": new_password, "name": new_name})
    print("succesfully created " + str(number_students) + " users")
    return Response({"users": new_students})

class StudentViewSet(viewsets.ViewSet):
    def list(self, request):
        classroom = Classroom.objects.get(code=request.query_params['code'])
        queryset = Enroll.objects.filter(classroom=classroom)
        students = []
        for enroll in queryset:
            student = StudentSerializer(enroll).data
            student['id'] = student['studentIndex']
            students.append(student)
        return Response(students)
    def update(self, request, **kwargs):
        verify_classroom_owner(request.data['code'], request.user)
        classroom = Classroom.objects.get(code=request.data['code'])
        profile = Enroll.objects.get(classroom=classroom, studentIndex=request.data['index'])
        
        student_user = profile.studentUserID
        student_user.first_name = request.data['name']
        student_user.save()

        profile.name = request.data['name']
        profile.save()

        return Response('done')

class TaskViewSet(viewsets.ViewSet):
    '''
    Relates to tasks management, accessible only by teachers and admins, has 4 methods:
    1. List - obtains a list of all tasks
    2. Create - creates a new task, with the option to publish at a later date, and to create multiple tasks at once
    3. Update - allows tasks to be updated
    4. Delete - deletes task based on the task ID
    '''

    def list(self, request):
        if 'code' in request.query_params:
            # If class code is defined, it returns all tasks set in that class
            classroom = Classroom.objects.get(
                code=request.query_params['code'])
            queryset = Task.objects.filter(
                classroom=classroom, classroom__teacher=request.user)
        else:
            # Otherwise, it returns all tasks set by the teacher
            queryset = Task.objects.filter(classroom__teacher=request.user)

        return Response(TaskSerializer(queryset, many=True).data)

    def create(self, request):
        def add_task(task_data):
            # Obtains task data - code, name of task, task description, max number of stars
            task = Task(
                classroom=Classroom.objects.get(code=task_data['code']),
                name=task_data['name'],
                description=task_data['description'],
                max_stars=5,
                is_group=task_data['isGroupSubmission']
            )

            if 'display' in task_data:
                # Checks the display status - determines whether task will be published on creation
                task.display = task_data['display']
                if task_data['display'] == 1:
                    task.published_at = timezone.now()
                    
            else:
                # If no display value is present, task is published by default
                task.published_at = timezone.now()

            task.save()
            return task

        if 'bulk' not in request.query_params:
            # Checks whether tasks will be bulk published - by default, it is not
            task = add_task(request.data)
            return Response(TaskSerializer(task).data)
        else:
            # Bulk add tasks
            tasks = [add_task(task_data) for task_data in request.data]
            return Response(TaskSerializer(tasks, many=True).data)

    def update(self, request, **kwargs):
        task = Task.objects.get(pk=int(kwargs['pk']))

        verify_classroom_owner(task.classroom.code, request.user)

        # Sets the new task data, obtaining at least one of the four pieces of information: name, description, status or max stars
        task.name = request.data['name']
        task.description = request.data['description']
        task.status = request.data['status']
        task.max_stars = request.data['max_stars']
        task.is_group_task = request.data['is_group_task']

        if 'display' in request.data:
            # Allows for tasks to be published
            task.display = request.data['display']

            if task.published_at is None and task.display == 1:
                task.published_at = timezone.now()

        task.save()

        return Response(TaskSerializer(task).data)

    def delete(self, request, **kwargs):
        # Deletes task based on ID
        task = Task.objects.get(pk=int(kwargs['pk']))

        verify_classroom_owner(task.classroom.code, request.user)

        task.delete()

        return Response("task deleted")

class SubmissionViewSet(viewsets.ViewSet):
    '''
    Relates to all submissions, accessible by teachers and admins, has 2 methods:
    1. List - obtains all tasks assigned to the classroom
    2. Update - Allows teachers to update the number of stars and comments for a task
    '''

    def list(self, request):
        # All submissions from classroom based on the classroom code
        tasks = Classroom.objects.get(
            code=request.query_params['code']).task_set.all()

        # no idea what this does but im guessing it orders submissions by tasks
        subs_by_task = [task.submission_set.all()
                        for task in tasks if task.submission_set.all()]

        # and that this gets a list of all submissions for a specific task
        subs = [item for sublist in subs_by_task for item in sublist]

        return Response(SubmissionSerializer(subs, many=True).data)

    def update(self, request, **kwargs):
        sub = Submission.objects.get(pk=int(kwargs['pk']))

        verify_classroom_owner(sub.task.classroom.code, request.user)

        # in case review accidentally submitted twice
        # not sure why this if check is needed tho
        if sub.stars != request.data['stars']:
            sub.stars = request.data['stars']
            sub.comments = request.data['comment']
            sub.save()

        return Response(SubmissionSerializer(sub).data)

class SubmissionStatusViewSet(viewsets.ViewSet):
    '''
    Allows teachers to see the submission status of all tasks for all students in a class
    '''

    def list(self, request):
        # All submission statuses from classroom
        tasks = Classroom.objects.get(
            code=request.query_params['code']).task_set.all()
        statuses_by_task = [task.submissionstatus_set.all()
                            for task in tasks if task.submissionstatus_set.all()]
        statuses = [
            item for statuslist in statuses_by_task for item in statuslist]

        return Response(SubmissionStatusSerializer(statuses, many=True).data)

class AnnouncementViewSet(viewsets.ViewSet):
    '''
    Relates to announcements, accessible by teachers and admins, has 4 methods:
    1. List - obtains a list of all announcements for a specific class
    2. Create - allows teachers to create a new announcement
    3. Update - allows teachers to update details of an announcement
    4. Delete - allows teachers to delete an announcement
    '''

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
    # I think this displays all the information relating to resources in the dashboard?
    '''
    Relates to viewing all resources for a specific class, and how it is stored in the DB, has 3 methods:
    1. List - obtains all resources posted to the classroom
    2. Create - Stores it in a database that contains information on all resources, regardless of classroom
    3. Destroy - removes a resource from the class
    '''
    # def __init__(self, *args, **kwargs):
    #     file_fields = kwargs.pop('file_fields', None)
    #     super().__init__(*args, **kwargs)
    #     if file_fields:
    #         field_update_dict = {field: serializers.FileField(required=False, write_only=True) for field in file_fields}
    #         self.fields.update(**field_update_dict)

    def list(self, request):
        # Obtains a list of all resources posted based on classroom code
        classroom = Classroom.objects.get(code=request.query_params['code'])
        sections = ResourceSection.objects.filter(classroom=classroom)
        resources = [{
            "section": ResourceSectionSerializer(section).data,
            "resources": ResourceSerializer(section.resource_set, many=True).data
        } for section in sections]

        return Response(resources)

    def create(self, request):
        # Creates a new entry in the database
        # Gets object data for a classroom
        classroom = Classroom.objects.get(code=request.data['code'])

        # Initializes a new resource group for that classroom and saves it
        section = ResourceSection(
            classroom=classroom, name=request.data['name'])
        section.save()

        # Creates a list of all resources for that classroom
        res_list = []

        # Not sure where the key comes from
        for key, file in request.data.items():

            # Checks that file is present in the key
            if 'file' in key:
                # Creates a new resource entry and saves it
                res = Resource(section=section, name=file.name)
                res.save()

                # Formats the filename and saves it, then appends it to the list
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
        # Deletes the resource section from the classroom
        rs = ResourceSection.objects.get(pk=int(kwargs['pk']))

        verify_classroom_owner(rs.classroom.code, request.user)

        rs.delete()

        return Response(True)

class ResourceViewSet(viewsets.ViewSet):
    # And this one relates to displaying an individual resource
    '''
    Relates to a specific resource and how it is displayed, has 3 methods:
    1. Obtains all attributes relating to a specific resource
    2. Allows for the creation of a new resource
    3. Deletes the specific resource from the classroom
    '''

    def retrieve(self, request, **kwargs):
        # Obtains a list of all resources
        resource = Resource.objects.get(id=kwargs['pk'])
        verify_classroom_owner(resource.section.classroom.code, request.user)
        return Response(ResourceSerializer(resource).data)

    def create(self, request):
        # Creates a new resource
        section = ResourceSection.objects.get(
            id=request.data['resource_section_id'])

        verify_classroom_owner(section.classroom.code, request.user)

        # Obtains the data from the new file and saves it
        new_file = request.data['file']
        res = Resource(section=section, name=new_file.name)
        res.save()

        # Formats the file name and saves it
        filename = 'res_{}_{}_{}'.format(
            section.id, res.id, new_file.name
        )
        res.file.save(filename, ContentFile(new_file.read()))

        return Response(ResourceSerializer(res).data)

    def destroy(self, request, **kwargs):
        # Deletes a file based on the PK
        res = Resource.objects.get(pk=int(kwargs['pk']))

        verify_classroom_owner(res.section.classroom.code, request.user)

        res.delete()

        return Response(True)
