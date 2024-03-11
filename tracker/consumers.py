import json

from channels.generic.websocket import AsyncWebsocketConsumer
from django.db.utils import OperationalError


class TaskUpdateConsumerV2(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]

        if self.user.is_authenticated:
            # Create a unique room group name based on the user's identifier
            self.room_group_name = f"user_{self.user.id}"

            # Add the user to the room group
            await self.channel_layer.group_add(self.room_group_name, self.channel_name)

            # Accept the WebSocket connection
            await self.accept()
        else:
            await self.close()

    async def disconnect(self, close_code):
        if hasattr(self, 'room_group_name'):
            # Remove the user from the room group upon disconnection
            await self.channel_layer.group_discard(
                self.room_group_name, self.channel_name
            )
            await self.close()

    async def task_thread(self, event):
        try:
            text_message = event['message']
            await self.send(text_data=json.dumps({'message': text_message}))
        except OperationalError:
            pass
