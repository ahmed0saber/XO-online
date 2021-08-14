from channels.generic.websocket import AsyncWebsocketConsumer
import json


class GameConsumer(AsyncWebsocketConsumer):

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