from django.db.models.signals import post_save
from django.dispatch import receiver

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from core.models import Task, Submission, Announcement
from core.serializers import TaskSerializer, SubmissionSerializer, AnnouncementSerializer
from student_core.models import Enroll

@receiver(post_save, sender=Task)
def send_task(sender, instance, **kwargs):
    # New tasks or task updates will be sent to students

    if instance.display == 1: # draft tasks will not be sent
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'student_{}'.format(instance.classroom.code),
            {"type": "send_task", "task": TaskSerializer(instance).data},
        )

@receiver(post_save, sender=Submission)
def send_submission(sender, instance, created, **kwargs):
    if instance.stars is not None:
        ## Update score once teacher reviewed
        sp = Enroll.objects.get(studentUserID=instance.student, classroom=instance.task.classroom)
        sp.score += instance.stars
        sp.save()

        # Send comments to the student
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'student_{}'.format(instance.student.id),
            {"type": "send_submission", "submission": SubmissionSerializer(instance).data},
        )

@receiver(post_save, sender=Announcement)
def send_announcement(sender, instance, created, **kwargs):
    ## Send new announcements and updates to students
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'student_{}'.format(instance.classroom.code),
        {"type": "send_announcement", "announcement": AnnouncementSerializer(instance).data},
    )
