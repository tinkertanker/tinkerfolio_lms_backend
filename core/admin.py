from django.contrib import admin
from .models import *

@admin.register(Classroom)
class ClassroomAdmin(admin.ModelAdmin):
    search_fields = ['id', 'name', 'teacher__id']

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    search_fields = ['id', 'name', 'classroom__name']

@admin.register(SubmissionStatus)
class SubmissionStatusAdmin(admin.ModelAdmin):
    search_fields = ['id', 'student__id', 'task__name']

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    search_fields = ['task__name', 'id', 'student__id']

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    search_fields = ['id', 'name', 'classroom__name']

@admin.register(ResourceSection)
class ResourceSectionAdmin(admin.ModelAdmin):
    search_fields = ['id', 'name', 'classroom__name']

@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    search_fields = ['id', 'name', 'section__name']

@admin.register(Enroll)
class Enroll(admin.ModelAdmin):
    search_fields = ['studentUserID', 'classroom', 'studentIndex' ]