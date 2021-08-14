from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    USER_TYPES = (
        (1, 'student'),
        (2, 'teacher')
    )

    user_type = models.PositiveSmallIntegerField(choices=USER_TYPES, default=2)

class StudentProfile(models.Model):
    student = models.OneToOneField(User, on_delete=models.CASCADE)
    assigned_class_code = models.CharField(max_length=6)
    index = models.IntegerField()
    name = models.CharField(max_length=200, default="")
    score = models.IntegerField(default=0)
