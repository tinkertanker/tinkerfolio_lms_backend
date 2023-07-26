from rest_framework.test import APIClient, force_authenticate
from rest_framework import status
from django.test import TestCase
from core.models import Classroom
from student_core.models import Enroll
from django.contrib.auth import get_user_model
from student_core.views import EnrollViewSet
from rest_framework.response import Response

User = get_user_model()

class EnrollViewSetTestCase(TestCase):
    def setUp(self):
        self.teacher = User.objects.create_user(username='teacher', password='teacherpassword', user_type=2)

        self.student = User.objects.create_user(username='student', password='studentpassword', user_type=1)

        self.client = APIClient()
        self.client.force_authenticate(user=self.teacher)
        self.classroom = Classroom.objects.create(teacher=self.teacher, name='Test Classroom', code='testcode')

        self.client = APIClient()
        self.client.force_authenticate(user=self.student)

    def test_student_join_course_success(self):
        url = '/student/enroll/'

        data = {
            'code': self.classroom.code,
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        enrollment = Enroll.objects.filter(classroom=self.classroom, studentUserID=self.student).first()
        self.assertIsNotNone(enrollment)

    def test_student_join_course_already_enrolled(self):
        Enroll.objects.create(classroom=self.classroom, studentUserID=self.student, studentIndex=1, score=0)

        url = '/student/enroll/'

        data = {
            'code': self.classroom.code,
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data, 'Student is already in the classroom.')

    def test_list_student_classrooms(self):
        classroom1 = Classroom.objects.create(teacher=self.teacher, name='Classroom 1', code='class1')
        classroom2 = Classroom.objects.create(teacher=self.teacher, name='Classroom 2', code='class2')
        Enroll.objects.create(classroom=classroom1, studentUserID=self.student, studentIndex=1, score=0)
        Enroll.objects.create(classroom=classroom2, studentUserID=self.student, studentIndex=2, score=0)

        url = '/student/enroll/'

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2) 

    