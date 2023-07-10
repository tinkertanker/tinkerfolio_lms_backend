from django.db import models
from accounts.models import User
from core.models import Classroom

# Create your models here.
class Enroll(models.Model):
    def __str__(self):
        return str(self.studentUserID) + ', Classroom: ' + str(self.classroom) 

    student_user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    studentIndex = models.IntegerField()
    score = models.IntegerField(default=0)

class StudentGroup(models.Model):
    # for student groups to work, you need the classroom code, the group number, 
    # and the index number of the students
    # uniquely identified by the classroom code and group number

    class Meta:
        constraints=[
            models.UniqueConstraint(fields = ['classroom', 'group_number'], name = 'unique_identifier')
        ]

    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    group_number = models.PositiveSmallIntegerField()

    member_indexes = models.JSONField(default=list)