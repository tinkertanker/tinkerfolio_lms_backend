from django.db.models.signals import post_save
from django.dispatch import receiver

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from accounts.models import StudentProfile
from core.models import Submission, SubmissionStatus
from core.serializers import SubmissionSerializer, SubmissionStatusSerializer, StudentProfileSerializer

@receiver(post_save, sender=Submission)
def send_submission(sender, instance, created, **kwargs):
    ## New submissions by students will be sent to teacher
    if created:
        print('is created')
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'teacher_{}'.format(instance.task.classroom.code),
            {"type": "send_submission", "submission": SubmissionSerializer(instance).data},
        )

@receiver(post_save, sender=SubmissionStatus)
def send_submission_status(sender, instance, created, **kwargs):
    ## changes to submission status will be pushed to teacher
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'teacher_{}'.format(instance.task.classroom.code),
        {"type": "send_submission_status", "submission_status": SubmissionStatusSerializer(instance).data},
    )

@receiver(post_save, sender=StudentProfile)
def send_student_profile(sender, instance, created, **kwargs):
    ## When a student signs up
    if created:
        if instance.created_by_student:
            profile = StudentProfileSerializer(instance).data
            profile['id'] = instance.student.id

            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                'teacher_{}'.format(instance.assigned_class_code),
                {"type": "send_student_profile", "student_profile": profile},
            )
