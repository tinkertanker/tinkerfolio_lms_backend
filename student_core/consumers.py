import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from urllib.parse import parse_qs

class StudentConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        if self.user.user_type != 1:
            await self.close()

        ## Classroom group
        code = await self.get_class_code()
        await self.channel_layer.group_add(
            'student_{}'.format(code),
            self.channel_name
        )
        ## Individual student group
        await self.channel_layer.group_add(
            'student_{}'.format(self.user.id),
            self.channel_name
        )

        await self.accept()

    @database_sync_to_async
    def get_class_code(self):
        self.code = parse_qs(self.scope["query_string"].decode("utf8"))["code"][0]
        return self.code
        # return self.user.studentprofile.assigned_class_code

    async def disconnect(self, close_code):
        pass

    async def send_task(self, event):
        task = event['task']
        await self.send(text_data=json.dumps({
            'task': task
        }))

    async def send_submission(self, event):
        submission = event['submission']
        await self.send(text_data=json.dumps({
            'submission': submission
        }))

    async def send_announcement(self, event):
        announcement = event['announcement']
        await self.send(text_data=json.dumps({
            'announcement': announcement
        }))
