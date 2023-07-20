from django.db import models
from accounts.models import User
from core.models import Classroom

# Create your models here.
class Enroll(models.Model):
    def __str__(self):
        return str(self.studentUserID) + ', Classroom: ' + str(self.classroom) 

    studentUserID = models.ForeignKey(User, on_delete=models.CASCADE)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    studentIndex = models.IntegerField()
    score = models.IntegerField(default=0)
