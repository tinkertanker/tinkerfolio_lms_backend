from rest_framework import serializers

from core.models import Classroom, Task, Submission, SubmissionStatus, Announcement, ResourceSection, Resource
from accounts.models import StudentProfile
from student_core.models import Enroll

class EnrollSerializer(serializers.ModelSerializer):
    classroom = serializers.SerializerMethodField()

    class Meta:
        model = Enroll
        fields = '__all__'

    # since classroom is a foreign key, we need to serialize it
    def get_classroom(self, enroll):
        return ClassroomSerializer(enroll.classroom).data
    
class ClassroomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classroom
        fields = '__all__'

class StudentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentProfile
        fields = ['index', 'name', 'score']

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'

class SubmissionStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubmissionStatus
        fields = '__all__'

class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = '__all__'

class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = '__all__'

class ResourceSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResourceSection
        fields = '__all__'

class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = '__all__'
