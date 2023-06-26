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

class StudentSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = Enroll
        fields = ['studentUserID', 'studentIndex', 'score', 'name']

    def get_name(self, obj):
        return f"{obj.studentUserID.first_name} {obj.studentUserID.last_name}"

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'

class SubmissionStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubmissionStatus
        fields = '__all__'

class InputObjectField(serializers.Field):
    def to_representation(self, value):
        input_object = {}
        input_object['image'] = value.image.url if value.image else None
        input_object['text'] = value.text
        return input_object
    
class StudentSubmissionSerializer(serializers.ModelSerializer):
    taskName = serializers.CharField(source='task.name')
    className = serializers.CharField(source='task.classroom.name')
    inputObject = serializers.SerializerMethodField()
    
    def get_inputObject(self, submission):
        # Determine the input object based on the existence of the image field
        if submission.image:
            # If image field exists, return the image file
            return submission.image
        else:
            # If image field does not exist, return the text field
            return submission.text

    class Meta:
        model = Submission
        fields = ['taskName', 'className', 'inputObject']

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
