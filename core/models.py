from django.db import models
from accounts.models import User

# Create your models here.
class Classroom(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=6)

class Task(models.Model):
    STATUS_TYPES = (
        (1, 'In Progress'),
        (2, 'Completed')
    )

    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)

    name = models.CharField(max_length=200)
    description = models.TextField()
    status_type = models.PositiveSmallIntegerField(choices=STATUS_TYPES, default=1)
    max_starts = models.IntegerField()

class Submission(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)

    image = models.ImageField(blank=True, null=True)
    text = models.TextField(blank=True, null=True)

    stars = models.IntegerField(blank=True, null=True)
    comments = models.TextField(blank=True, null=True)
