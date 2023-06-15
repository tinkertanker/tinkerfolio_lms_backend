from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(Enroll)
class Enroll(admin.ModelAdmin):
    search_fields = ['studentUserID', 'classroom', 'studentIndex', 'score']
