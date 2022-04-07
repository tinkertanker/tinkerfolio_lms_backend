from django.db.models.signals import post_save
from django.dispatch import receiver

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from core.models import Task, Submission
from core.serializers import TaskSerializer, SubmissionSerializer

@receiver(post_save, sender=Task)
def send_task(sender, instance, **kwargs):
    # New tasks or task updates will be sent to students
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'student_{}'.format(instance.classroom.code),
        {"type": "send_task", "task": TaskSerializer(instance).data},
    )

@receiver(post_save, sender=Submission)
def send_submission(sender, instance, created, **kwargs):
    ## If teacher comments, sent them to student

    if instance.stars is not None:
        ## Update score
        sp = instance.student.studentprofile
        sp.score += instance.stars
        sp.save()

        ## Send comments to student
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'student_{}'.format(instance.student.id),
            {"type": "send_submission", "submission": SubmissionSerializer(instance).data},
        )
