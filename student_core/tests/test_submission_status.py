from rest_framework.test import APIClient
from rest_framework import status
from django.test import TestCase
from core.models import Classroom, Task, SubmissionStatus
from student_core.models import Enroll
from django.contrib.auth import get_user_model
User = get_user_model()

class StudentSubmissionStatusViewSetTestCase(TestCase):
    def setUp(self):
        self.teacher = User.objects.create_user(username='teacher', password='teacherpassword', user_type=2)

        self.student = User.objects.create_user(username='student', password='studentpassword', user_type=1, first_name='Student 1')

        self.client = APIClient()
        self.client.force_authenticate(user=self.teacher)
        self.classroom = Classroom.objects.create(teacher=self.teacher, name='Test Classroom', code='testcode')

        Enroll.objects.create(classroom=self.classroom, studentUserID=self.student, studentIndex=1)

        self.task = Task.objects.create(classroom=self.classroom, name='Test Task', description='This is a test task.', display=1, max_stars=5)

        self.client = APIClient()
        self.client.force_authenticate(user=self.student)

    def test_create_submission_status(self):
        url = '/student/submission_status/'

        data = {
            'task_id': self.task.id,
            'student': self.student.id,
            'status': 1,
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_data = {
            'id': self.task.id,
            'status': 1,
            'task': self.task.id,
            'student': self.student.id,
        }
        self.assertEqual(response.data, expected_data)

    def test_update_submission_status(self):
        submission_status = SubmissionStatus.objects.create(task=self.task, student=self.student, status=1)

        url = f'/student/submission_status/{submission_status.id}/'

        data = {
            'status': 2,  
        }

        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_data = {
            'id': self.task.id,
            'status': 2,  
            'task': self.task.id,
            'student': self.student.id,
        }
        self.assertEqual(response.data, expected_data)
