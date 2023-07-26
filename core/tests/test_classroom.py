from rest_framework.test import APIClient, force_authenticate

from rest_framework import status
from django.test import TestCase
from django.contrib.auth import get_user_model
from core.models import Classroom

User = get_user_model()

class ClassroomViewSetTestCase(TestCase):
    def setUp(self):
        self.teacher = User.objects.create_user(username='teacher', password='teacherpassword', user_type=2)
        self.client = APIClient()
        self.client.login(username='teacher', password='teacherpassword')

    def test_list_classrooms(self):
        classroom = Classroom.objects.create(teacher=self.teacher, name='Test Classroom', code='testcode')

        url = '/core/classrooms/'

        self.client.force_authenticate(user=self.teacher)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Test Classroom')

    def test_retrieve_classroom(self):
        classroom = Classroom.objects.create(teacher=self.teacher, name='Test Classroom', code='testcode')

        url = f'/core/classrooms/{classroom.code}/'

        self.client.force_authenticate(user=self.teacher)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Classroom')

