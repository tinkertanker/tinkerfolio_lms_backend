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
