from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        (1, 'student'),
        (2, 'teacher')
    )

    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, default=2)
