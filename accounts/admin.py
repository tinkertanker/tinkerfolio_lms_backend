from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from .models import *

@admin.register(User)
class UserAdmin(UserAdmin):
    list_display= [f.name for f in User._meta.fields]
    list_filter = ['user_type']
    search_fields = ['username', 'first_name', 'last_name', 'email']

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('User Type', {
            'fields': ('user_type',)
        }),
    )

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
