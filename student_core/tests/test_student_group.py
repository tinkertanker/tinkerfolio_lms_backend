from rest_framework.test import APIClient, force_authenticate
from rest_framework import status
from django.test import TestCase
from core.models import Classroom, ResourceSection, Resource, Task, Submission, SubmissionStatus, Announcement
from student_core.models import Enroll
from django.contrib.auth import get_user_model
User = get_user_model()

class GroupSubmissionViewSetTestCase(TestCase):
    def setUp(self):
        self.teacher = User.objects.create_user(username='teacher', password='teacherpassword', user_type=2)

        self.student1 = User.objects.create_user(username='student1', password='student1password', user_type=1, first_name='Student 1')
        self.student2 = User.objects.create_user(username='student2', password='student2password', user_type=1, first_name='Student 2')

        self.client = APIClient()
        self.client.force_authenticate(user=self.teacher)
        self.classroom = Classroom.objects.create(teacher=self.teacher, name='Test Classroom', code='testcode')

        self.task = Task.objects.create(classroom=self.classroom, name='Test Task', description='This is a test task.', display=1, max_stars=5)

        self.client = APIClient()
        self.client.force_authenticate(user=self.student1)

    def test_create_group_submission(self):
        url = '/student/group_submission/'

        data = {
            'task_id': self.task.id,
            'team_students': f'{self.student1.first_name}, {self.student2.first_name}',
            'text': 'Group submission text.'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        