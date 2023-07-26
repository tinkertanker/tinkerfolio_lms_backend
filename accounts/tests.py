from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth.models import User
from accounts.views import StudentSignUp, TeacherSignUp
from accounts.models import User
import os 
import environ

env = environ.Env(
    DEBUG=(bool, False)
)
class TeacherSignUpTestCase(APITestCase):
    def setUp(self):
        self.test_user = User.objects.create_user(username='testuser', password='testpass')

        self.url = "/auth/token/teacher_signup/"

    def test_teacher_signup_success(self):
        data = {
            'username': 'newteacher',
            'email': 'newteacher@example.com',
            'first_name': 'John',
            'password': 'testpass',
            'passcode': env('PASSCODE') 
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
            'Account': 'Teacher',
            'Username': data['username'],
            'First Name': data['first_name']
        })

        teacher_user = User.objects.get(username=data['username'])
        self.assertEqual(teacher_user.email, data['email'])
        self.assertEqual(teacher_user.first_name, data['first_name'])
        self.assertEqual(teacher_user.user_type, 2)  

        self.assertNotEqual(teacher_user, self.test_user)


    def test_teacher_signup_existing_username(self):
        User.objects.create_user(username='existinguser', password='existingpass', first_name="existingname")

        data = {
            'username': 'existinguser',  
            'email': 'newteacher@example.com',
            'first_name': 'John',
            'password': 'testpass',
            'passcode': env('PASSCODE')
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'error': 'Username already exists.'})


class StudentSignUpTestCase(APITestCase):
    def setUp(self):
        self.test_user = User.objects.create_user(username='testuser', password='testpass')

        self.url = "/auth/token/student_signup/"

    def test_student_signup_success(self):
        data = {
            'username': 'newstudent',
            'email': 'newstudent@example.com',
            'first_name': 'Jane',
            'password': 'testpass',
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
            'Account': 'Student',
            'Username': data['username'],
            'First Name': data['first_name']
        })

        student_user = User.objects.get(username=data['username'])
        self.assertEqual(student_user.email, data['email'])
        self.assertEqual(student_user.first_name, data['first_name'])
        self.assertEqual(student_user.user_type, 1)

        self.assertNotEqual(student_user, self.test_user)

    def test_student_signup_existing_username(self):
        User.objects.create_user(username='existingstudent', password='existingpass', first_name="existingname")

        data = {
            'username': 'existingstudent',
            'email': 'newstudent@example.com',
            'first_name': 'Jane',
            'password': 'testpass',
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'error': 'Username already exists.'})
