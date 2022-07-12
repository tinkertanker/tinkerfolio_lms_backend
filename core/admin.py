from django.contrib import admin
from .models import *

@admin.register(Classroom)
class ClassroomAdmin(admin.ModelAdmin):
    pass

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    pass

@admin.register(SubmissionStatus)
class SubmissionStatusAdmin(admin.ModelAdmin):
    pass

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    pass

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    pass

@admin.register(ResourceSection)
class ResourceSectionAdmin(admin.ModelAdmin):
    pass

@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    pass
