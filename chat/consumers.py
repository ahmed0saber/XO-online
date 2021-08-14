import json
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import global_message
from .serializers import messageSerializer


class GlobalChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = 'global'
        self.room_group_name = 'global'
        if self.scope['user'].is_authenticated:

            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )

            await self.accept()
        else:
            self.close()


    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    @database_sync_to_async
    def create_message(self, content):

        new_message = global_message.objects.create(sender=self.scope['user'], content=content)
        new_message.save()
        return new_message

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        message = await self.create_message(message)
        serializer = messageSerializer(message)
        context = {"type":"chat_message"}
        context.update(serializer.data)
        
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            context
        )

    

    
    # Receive message from room group
    async def chat_message(self, event):

        # Send message to WebSocket
        await self.send(text_data=json.dumps(event))