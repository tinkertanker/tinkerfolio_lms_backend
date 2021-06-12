from django.db.models.signals import post_save
from django.dispatch import receiver

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from core.models import Submission
from core.serializers import TaskSerializer, SubmissionSerializer

@receiver(post_save, sender=Submission)
def send_submission(sender, instance, created, **kwargs):
    ## New submissions by students will be sent to teacher
    if created:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'teacher_{}'.format(instance.task.classroom.code),
            {"type": "send_submission", "submission": SubmissionSerializer(instance).data},
        )
