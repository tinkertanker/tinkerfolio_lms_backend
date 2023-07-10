from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    REQUIRED_FIELDS = [ 'first_name', 'email' ]

    def __str__(self):
        # Temp Student Account
        if self.user_type == 1:
            return '[Student] ' + self.username + ' (ID: '+ str(self.id) + ')'
            
        # Perm Teacher Account
        if self.user_type == 2:
            return '[Teacher] ' + self.username + ' (ID: '+ str(self.id) + ')'
            

    USER_TYPES = (
        (1, 'student'),
        (2, 'teacher')
    )

    user_type = models.PositiveSmallIntegerField(choices=USER_TYPES,default=2)
    first_name = models.CharField(max_length=150, blank=False, null=False)
    email = models.EmailField(blank=False, null=False)

# class StudentProfile(models.Model):

#     def __str__(self):
#         return self.name+' (Class: '+self.assigned_class_code+'; Index: '+str(self.index)+')'

#     student = models.OneToOneField(User, on_delete=models.CASCADE)
#     assigned_class_code = models.CharField(max_length=6)
#     index = models.IntegerField()
#     name = models.CharField(max_length=200, default="")
#     score = models.IntegerField(default=0)
#     created_by_student = models.BooleanField(default=False)
