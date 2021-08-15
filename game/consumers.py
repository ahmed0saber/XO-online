from channels.generic.websocket import AsyncWebsocketConsumer
import json


class GameConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room']
        self.room_group_name = 'game_' + self.room_name
        connected_count = len(self.channel_layer.groups.get(self.room_group_name, {}).items())
        if connected_count > 1:
            await self.accept()
            await self.send(text_data=json.dumps({'error': 'this room is already full try to connect to different room'}))
            await self.close()
            return
        if self.scope['user'].is_authenticated:
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()
            await self.send(json.dumps({'first': connected_count == 0}))
        else:
            await self.close()

    
    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type':'user_left'
            }
        )
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
    async def receive(self, text_data):
        text_data = json.loads(text_data)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type':'game_play',
                'player':text_data['player'],
                'move':text_data['move']
            }
        )
    

    async def game_play(self, event):
        await self.send(text_data=json.dumps(event))
    
    async def user_left(self, event):
        await self.send(json.dumps(event))