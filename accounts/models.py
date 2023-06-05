from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):

    def __str__(self):
        # Temp Student Account
        if self.user_type == 1:
            try:
                return self.studentprofile.name+' [Temporary Student] Class: ' + self.studentprofile.assigned_class_code + '; Index: ' + str(self.studentprofile.index)
            except:
                return 'Student (no profile)'
            
        # Perm Teacher Account
        if self.user_type == 2:
            return '[Teacher] ' + self.username + ' (ID: '+ str(self.id) + ')'
        

        # Perm Student Account
        if self.user_type == 3:
            return '[Student] ' + self.username + ' (ID: '+ str(self.id) + ')'
            

    USER_TYPES = (
        (1, 'temporaryStudentAccount'),
        (2, 'teacher'),
        (3, 'student')
    )

    user_type = models.PositiveSmallIntegerField(choices=USER_TYPES,default=2)

class StudentProfile(models.Model):

    def __str__(self):
        return self.name+' (Class: '+self.assigned_class_code+'; Index: '+str(self.index)+')'

    student = models.OneToOneField(User, on_delete=models.CASCADE)
    assigned_class_code = models.CharField(max_length=6)
    index = models.IntegerField()
    name = models.CharField(max_length=200, default="")
    score = models.IntegerField(default=0)
    created_by_student = models.BooleanField(default=False)
