from django.contrib import admin
from .models import *

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_filter = ['user_type']
    search_fields = ['id', 'studentprofile__index', 'studentprofile__assigned_class_code', 'studentprofile__name']

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    search_fields = ['id', 'index', 'assigned_class_code', 'name']
