import json
from rest_framework.test import APIClient, force_authenticate
from rest_framework import status
from django.test import TestCase
from django.core.files.base import ContentFile
from core.models import Classroom, Task, Submission, SubmissionStatus
from student_core.models import Enroll
from django.contrib.auth import get_user_model
User = get_user_model()

class StudentSubmissionViewSetTestCase(TestCase):
    def setUp(self):
        self.teacher = User.objects.create_user(username='teacher', password='teacherpassword', user_type=2)

        self.student = User.objects.create_user(username='student', password='studentpassword', user_type=1)

        self.client = APIClient()
        self.client.force_authenticate(user=self.teacher)
        self.classroom = Classroom.objects.create(teacher=self.teacher, name='Test Classroom', code='testcode')

        self.enroll = Enroll.objects.create(classroom=self.classroom, studentUserID=self.student, studentIndex=1)

        self.task = Task.objects.create(classroom=self.classroom, name='Test Task', description='This is a test task.', display=1, max_stars=5)

        self.client = APIClient()
        self.client.force_authenticate(user=self.student)

    def test_create_submission(self):
        url = '/student/submission/'

        data = {
            'task_id': self.task.id,
            'text': 'Test submission text.',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if the submission exists in the database
        submission = Submission.objects.filter(student=self.student, task=self.task).first()
        self.assertIsNotNone(submission)

    def test_retrieve_submission(self):
        # Create a test submission
        submission = Submission.objects.create(task=self.task, student=self.student, text='Test submission text.')

        url = f'/student/submission/{submission.id}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_data = {
            'id': submission.id,
            'task': self.task.id,
            'student': self.student.id,
            'text': 'Test submission text.',
            'image': None,
            'stars': None,
            'comments': None,
            'created_at': submission.created_at.isoformat(),
            'resubmitted_at': None,
            'task_name': self.task.name,
            'classroom_name': self.task.classroom.name,
        }

        # account for delay
        expected_data['created_at'] = response.data['created_at']
        self.assertEqual(response.data, expected_data)


    def test_update_submission(self):
        submission = Submission.objects.create(task=self.task, student=self.student, text='Test submission text.')

        url = f'/student/submission/{submission.id}/'
        data = {
            'text': 'Updated submission text.',
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        submission.refresh_from_db()
        self.assertEqual(submission.text, 'Updated submission text.')

        self.assertIsNone(submission.stars)
        self.assertIsNone(submission.comments)
