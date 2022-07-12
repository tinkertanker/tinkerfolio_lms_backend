from django.db import models
from accounts.models import User

# Create your models here.
class Classroom(models.Model):

    def __str__(self):
        return self.name + ' (User ID: ' + str(self.teacher.id) + ')'

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

    def __str__(self):
        return self.name + ' (Class: ' + self.classroom.name + ')'

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

    class Meta:
        verbose_name_plural = 'SubmissionStatuses'

    def __str__(self):
        return 'Student ID: ' + str(self.student.id) + '; Task: ' + self.task.name

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

    def __str__(self):
        return 'Student ID: ' + str(self.student.id) + '; Task: ' + self.task.name

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

    def __str__(self):
        return self.name + ' (Class: ' + self.classroom.name + ')'

    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=200)
    description = models.TextField()

class ResourceSection(models.Model):

    def __str__(self):
        return self.name + ' (Class: ' + self.classroom.name + '; ID: ' + str(self.id) + ')'

    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=200)

class Resource(models.Model):

    def __str__(self):
        return self.name + ' (Section: ' + self.section.name + '; ID: ' + str(self.id) + ')'

    section = models.ForeignKey(ResourceSection, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=200)
    ## File Name Format: (Resource Section ID)_(Resource ID)_(Resource Name).(format)
    file = models.FileField(blank=True, null=True, default=None)
