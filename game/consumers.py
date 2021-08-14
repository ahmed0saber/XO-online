from channels.generic.websocket import AsyncWebsocketConsumer
import json


class GameConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room']
        self.room_group_name = 'game_' + self.room_name
        if len(self.channel_layer.groups.get('self.room_group_name', {}).items()) > 1:
            await self.send(text_data=json.dumps({'error': 'this room is already full try to connect to different room'}))
            await self.close()
            return
        if self.scope['user'].is_authenticated:

            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )

            await self.accept()
            
        else:
            await self.send(text_data=json.dumps({'error': 'you have to login first to be able to play online'}))
            await self.close()

    
    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )