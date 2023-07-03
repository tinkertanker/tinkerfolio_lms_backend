from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from .models import *

@admin.register(User)
class UserAdmin(UserAdmin):
    list_filter = ['user_type']
    search_fields = ['id', 'studentprofile__index', 'studentprofile__assigned_class_code', 'studentprofile__name']

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('User Type', {
            'fields': ('user_type',)
        }),
    )

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    search_fields = ['id', 'index', 'assigned_class_code', 'name']

admin.site.unregister(User)
admin.site.register(User, UserAdmin)