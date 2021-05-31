from rest_framework import serializers

from core.models import Classroom
from accounts.models import StudentProfile

class ClassroomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classroom
        fields = '__all__'

class StudentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentProfile
        fields = ['index', 'name']
