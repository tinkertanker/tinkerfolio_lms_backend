import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer
from channels.db import database_sync_to_async
from urllib.parse import parse_qs

from core.models import Classroom, Submission
from core.serializers import SubmissionSerializer

class TeacherConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        self.code = parse_qs(self.scope["query_string"].decode("utf8"))["code"][0]

        ## Permissions
        if self.user.user_type != 2:
            await self.close()
        verified = await self.classroom_belongs_to_user()
        if not verified:
                        await self.close()

        ## Classroom group
        await self.channel_layer.group_add(
            'teacher_{}'.format(self.code),
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        # payload received from instructor
        text_data_json = json.loads(text_data)
        msg_type = list(text_data_json.keys())[0]

        if msg_type == "submission":
            sub = await self.get_submission(text_data_json['submission'])
            await self.send(text_data=json.dumps({
                'submission': SubmissionSerializer(sub).data
            }))

    async def send_submission(self, event):
        submission = event['submission']
        await self.send(text_data=json.dumps({
            'submission': submission
        }))

    async def send_submission_status(self, event):
        submission_status = event['submission_status']
        await self.send(text_data=json.dumps({
            'submission_status': submission_status
        }))

    async def send_student_profile(self, event):
        student_profile = event['student_profile']
        await self.send(text_data=json.dumps({
            'student_profile': student_profile
        }))

    @database_sync_to_async
    def classroom_belongs_to_user(self):
        classroom = Classroom.objects.get(code=self.code)
        if classroom.teacher != self.user:
            return False
        return True

    @database_sync_to_async
    def get_submission(self, id):
        return Submission.objects.get(id=id)

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        self.send(text_data=json.dumps({
            'message': message
        }))
