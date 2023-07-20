import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from urllib.parse import parse_qs
class StudentConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        self.code = parse_qs(self.scope["query_string"].decode("utf8"))["code"][0]

        ## Permissions
        if self.user.user_type != 1:
            await self.close()

        ## Classroom group
        await self.channel_layer.group_add(
            'student_{}'.format(self.code),
            self.channel_name
        )

        await self.accept()
