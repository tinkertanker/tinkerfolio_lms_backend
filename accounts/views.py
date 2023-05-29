from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from accounts.models import User, StudentProfile
from core.models import Classroom, Enroll


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

        enroll = Enroll(
            studentUserID=request.data['user_id'],classroom=request.data['code'], studentIndex=new_index
        )
        enroll.save()

        return Response({'code': request.data['code'], 'index': new_index})

class TeacherRegister(viewsets.ViewSet):
    permission_classes = [AllowAny]
    def create(self, request):
        teacher = User(username=request.data['username'], user_type=2, email=request.data['email'], first_name=request.data['first_name'], last_name=request.data['last_name'])
        teacher.set_password(request.data['password'])
        teacher.save()

        return Response({'Account': 'Teacher','Username': request.data['username'], 'First Name': request.data['first_name'], 'First Name': request.data['last_name']})


class StudentSignUp(viewsets.ViewSet):
    permission_classes = [AllowAny]
    def create(self, request):
        student = User(username=request.data['username'], user_type=3, email=request.data['email'], first_name=request.data['first_name'], last_name=request.data['last_name'])
        student.set_password(request.data['password'])
        student.save()

        return Response({'Account': 'Student','Username': 'username', 'First Name': 'first_name', 'Last Name': 'last_name'})

class StudentJoinClass(viewsets.ViewSet):
    permission_classes = [AllowAny]
    def create(self, request):
        enroll = Enroll(
            studentUserID=request.data['user_id'],classroom=request.data['code'], studentIndex=request.data['index']
        )
        enroll.save()

        return Response({'Student Account': 'studentUserId', 'Classroom': 'classroom', 'Index': 'studentIndex'})
