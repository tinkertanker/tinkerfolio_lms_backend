from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):

    def __str__(self):
        if self.user_type == 1:
            try:
                return self.studentprofile.name+' (Student; Class: '+self.studentprofile.assigned_class_code+'; Index: '+str(self.studentprofile.index)+')'
            except:
                return 'Student (no profile)'
        else:
            return self.username+' (ID: '+str(self.id)+')'

    USER_TYPES = (
        (1, 'student'),
        (2, 'teacher')
    )

    user_type = models.PositiveSmallIntegerField(choices=USER_TYPES, default=2)

class StudentProfile(models.Model):

    def __str__(self):
        return self.name+' (Class: '+self.assigned_class_code+'; Index: '+str(self.index)+')'

    student = models.OneToOneField(User, on_delete=models.CASCADE)
    assigned_class_code = models.CharField(max_length=6)
    index = models.IntegerField()
    name = models.CharField(max_length=200, default="")
    score = models.IntegerField(default=0)
    created_by_student = models.BooleanField(default=False)
