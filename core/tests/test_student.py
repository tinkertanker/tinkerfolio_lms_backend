from rest_framework.test import APIClient, force_authenticate
from rest_framework import status
from django.test import TestCase
from django.contrib.auth import get_user_model
from core.models import Classroom
from student_core.models import Enroll

User = get_user_model()

class StudentViewSetTestCase(TestCase):
    def setUp(self):
        self.teacher = User.objects.create_user(username='teacher', password='teacherpassword', user_type=2)
        self.client = APIClient()
        self.client.login(username='teacher', password='teacherpassword')

    def test_list_students(self):
        classroom = Classroom.objects.create(teacher=self.teacher, name='Test Classroom', code='testcode')

        student1 = User.objects.create(username='student1', user_type=1, first_name='Student 1')
        student2 = User.objects.create(username='student2', user_type=1, first_name='Student 2')
        Enroll.objects.create(classroom=classroom, studentUserID=student1, studentIndex=1)
        Enroll.objects.create(classroom=classroom, studentUserID=student2, studentIndex=2)


        url = f'/core/student_list/?code={classroom.code}'

        self.client.force_authenticate(user=self.teacher)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['name'].strip(), 'Student 1')
        self.assertEqual(response.data[1]['name'].strip(), 'Student 2')

    def test_update_student_name(self):
        classroom = Classroom.objects.create(teacher=self.teacher, name='Test Classroom', code='testcode')

        student = User.objects.create(username='student', user_type=1, first_name='Student 1')
        enroll = Enroll.objects.create(classroom=classroom, studentUserID=student, studentIndex=1)

        url = f'/core/student_list/update/'

        self.client.force_authenticate(user=self.teacher)

        data = {
            'code': classroom.code,
            'index': enroll.studentIndex,
            'name': 'New Student Name',
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        enroll.refresh_from_db()
        self.assertEqual(enroll.studentUserID.first_name, 'New Student Name')
