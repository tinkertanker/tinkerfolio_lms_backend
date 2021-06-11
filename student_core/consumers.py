import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

## test

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
        return self.user.studentprofile.assigned_class_code

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        await self.send(text_data=json.dumps({
            'message': message
        }))

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
