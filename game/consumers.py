from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from channels_presence.models import Room
from channels_presence.decorators import remove_presence, touch_presence
import json
import string 
import random


class GameConsumer(AsyncWebsocketConsumer):

    @database_sync_to_async
    def get_presences_count(self):
        try:
            return Room.objects.get(channel_name=self.room_group_name).presence_set.count()
        except:
            return 0


    @database_sync_to_async
    def add_to_group(self):
        Room.objects.add(self.room_group_name, self.channel_name, self.scope['user'])


    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room']
        if self.room_name == 'create':
            all = string.digits + string.ascii_letters
            name = random.choices(all, k=6)
            self.room_name = "".join(name)


        self.room_group_name = 'game_' + self.room_name
        connected_count =  await self.get_presences_count()
        if connected_count > 1:
            await self.accept()
            await self.send(text_data=json.dumps({
                'type':'error',
                'error': 'this room is already full try to connect to different room'
                }))
            await self.close()
            return
        if self.scope['user'].is_authenticated:
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()
            print(connected_count)
            await self.add_to_group()
            if connected_count == 1:
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type':'user_joined'
                    }
                )
        else:
            await self.close()

    @remove_presence
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
    
    @touch_presence
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
    
    async def user_joined(self, event):
        await self.send(json.dumps(event))