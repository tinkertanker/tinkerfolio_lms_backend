from django.db import models
from accounts.models import User
from core.models import Classroom

# Create your models here.
class Enroll(models.Model):
    def __str__(self):
        return self.studentUserID.name + ' (Classroom: ' + self.classroom.name + '; Index: ' + str(self.studentIndex) + ')'

    studentUserID = models.ForeignKey(User, on_delete=models.CASCADE)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    studentIndex = models.IntegerField()