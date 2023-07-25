from datetime import datetime
from rest_framework.test import APIClient, force_authenticate
from rest_framework import status
from django.test import TestCase
from django.contrib.auth import get_user_model
from core.models import Classroom, ResourceSection, Resource, Task, Submission, SubmissionStatus, Announcement
from student_core.models import Enroll
User = get_user_model()


class StudentInitialViewSetTestCase(TestCase):
    def setUp(self):
        self.student = User.objects.create_user(username='student', password='studentpassword', user_type=1)
        self.client = APIClient()
        self.client.force_authenticate(user=self.student)

    # initial without announcement, resource, task, submission, submission_status
    def test_list_student_initial_data(self):
        classroom = Classroom.objects.create(teacher=self.student, name='Test Classroom', code='testcode')

        enroll = Enroll.objects.create(classroom=classroom, studentUserID=self.student, studentIndex=1)

        url = f'/student/initial/?code={classroom.code}'

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        current_timestamp = datetime.now().isoformat()

        expected_data = {'profile': {'studentUserID': 1, 'studentIndex': 1, 'score': 0, 'name': ' '}, 'name': '', 
                        'classroom': {'id': 1, 'name': 'Test Classroom', 'code': 'testcode', 'student_indexes': [], 'status': 1, 'teacher': 1}, 
                        'announcements': [], 
                        'resources': [], 'tasks': [], 'submission_statuses': [], 
                        'submissions': []}

        response_data = response.data
        response_data['classroom'].pop('created_at', None)
        expected_data['classroom'].pop('created_at', None)

        self.maxDiff = None
        self.assertEqual(response_data, expected_data)
