from django.db.models.signals import post_save
from django.dispatch import receiver

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from core.models import Submission, SubmissionStatus
from core.serializers import SubmissionSerializer, SubmissionStatusSerializer

@receiver(post_save, sender=Submission)
def send_submission(sender, instance, created, **kwargs):
    ## New submissions and resubmissions by students will be sent to teacher
    if created or (instance.resubmitted_at and not instance.stars and not instance.comments):
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
