from django.db import models
from accounts.models import User

# Create your models here.
class Classroom(models.Model):
    STATUS_TYPES = (
        (1, 'Active'),
        (2, 'Archived')
    )

    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=6)
    student_indexes = models.JSONField(default=list)
    status = models.PositiveSmallIntegerField(choices=STATUS_TYPES, default=1)

    created_at = models.DateTimeField(auto_now_add=True)

class Task(models.Model):
    STATUS_TYPES = (
        (1, 'In Progress'),
        (2, 'Completed')
    )
    DISPLAY_TYPES = (
        (1, 'Published'),
        (2, 'Draft')
    )

    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)

    name = models.CharField(max_length=200)
    description = models.TextField()
    status = models.PositiveSmallIntegerField(choices=STATUS_TYPES, default=1)
    display = models.PositiveSmallIntegerField(choices=DISPLAY_TYPES, default=1)
    max_stars = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class SubmissionStatus(models.Model):
    ## completion status of student's task
    STATUS_TYPES = (
        (0, 'Not started'),
        (1, 'Working on it'),
        (2, 'Stuck')
    )

    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)

    status = models.PositiveSmallIntegerField(choices=STATUS_TYPES, default=0)

class Submission(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)

    ## Image Name Format: (Classroom Code)_(Task ID)_(Student ID).(format)
    image = models.ImageField(blank=True, null=True)
    text = models.TextField(blank=True, null=True)

    stars = models.IntegerField(blank=True, null=True)
    comments = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    resubmitted_at = models.DateTimeField(blank=True, null=True)

class Announcement(models.Model):
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=200)
    description = models.TextField()

class ResourceSection(models.Model):
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=200)

class Resource(models.Model):
    section = models.ForeignKey(ResourceSection, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=200)
    ## File Name Format: (Resource Section ID)_(Resource ID)_(Resource Name).(format)
    file = models.FileField(blank=True, null=True, default=None)
