from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from channels_presence.models import Room, Presence
from channels_presence.signals import presence_changed

from django.db.models import Q
from accounts.models import CustomUser
from chat.serializers import messageSenderSerializer
import json
import string 
import random


class GameConsumer(WebsocketConsumer):

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room']
        self.room_group_name = 'game_' + self.room_name
        self.accept()

        if self.room_name == 'create':
            all = string.digits + string.ascii_letters
            name = random.choices(all, k=6)
            self.room_name = "".join(name)
            self.room_group_name = 'game_' + self.room_name
            self.send(json.dumps({
                'type':'created',
                'room':self.room_name
            }))

            connected_count = 0
        else:
            try:
                connected_count = Room.objects.get(channel_name=self.room_group_name).presence_set.count()
            except:
                self.send(json.dumps({
                    'type':'error',
                    'code':'404',
                    'error': 'this room doesn\'t exist please make sure you typed the code right'
                    }))
                self.close()
                return
            else:
                if connected_count > 1:
                    self.send(text_data=json.dumps({
                    'type':'error',
                    'code':'420',
                    'error': 'this room is already full try to connect to different room'
                    }))
                    self.close()
                    return
        
        async_to_sync(self.channel_layer.group_add)(
        self.room_group_name,
        self.channel_name
        )
        Room.objects.add(self.room_group_name, self.channel_name, self.scope['user'])

        if connected_count == 1:
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type':'room_completed',
                }
            )
        

    
    def disconnect(self, close_code):
        # Leave room group
        try:
            player = Room.objects.get(channel_name=self.room_group_name).presence_set.filter(channel_name=self.channel_name)
            if player.exists():
                async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name,
                    {
                        'type':'error',
                        'code':'430',
                        'error':'user left the room. waiting for another user to join'
                    }
                )
                async_to_sync(self.channel_layer.group_discard)(
                    self.room_group_name,
                    self.channel_name
                )
                print('this is disconnecting')
                Room.objects.remove(self.room_group_name, self.channel_name)
        except:
            pass
        Room.objects.prune_presences()
        Room.objects.prune_rooms()
    
    
    def receive(self, text_data):
        player = Room.objects.get(channel_name=self.room_group_name).presence_set.filter(channel_name=self.channel_name)
        if not player.exists():
            self.send(json.dumps({
                'type':'error',
                'code':'408',
                'error':'Time out! You have to play in 15 seconds'
                }))
            self.close()
            return

        text_data = json.loads(text_data)
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            text_data
        )
        Presence.objects.touch(self.channel_name)

    
    def game_play(self, event):
        self.send(text_data=json.dumps(event))
    

    def error(self, event):
        self.send(json.dumps(event))

    def room_completed(self, event):
        user = self.scope['user']
        self_channel = Presence.objects.get(channel_name=self.channel_name)

        competitor = Room.objects.get(channel_name=self.room_group_name).presence_set.filter(~Q(channel_name=self_channel)).first().user
      
        if user.is_authenticated:
            serializer = messageSenderSerializer(instance=user)
            event.update({
                'self': serializer.data
            })
        else:
            event.update({
                'self': {
                    'front_id':None,
                    'image':CustomUser._meta.get_field("image").get_default(),
                    'name':'Unknown User',
                    'profile_url':"#"
                }
            })

        if competitor:
            serializer = messageSenderSerializer(instance=competitor)
            event.update({
                'competitor': serializer.data
            })
        else:
            event.update({
                'competitor': {
                    'front_id':None,
                    'image':CustomUser._meta.get_field("image").get_default(),
                    'name':'Unknown User',
                    'profile_url':"#"
                }
            })

        self.send(json.dumps(event))
    
    def restart(self, event):
        self.send(json.dumps(event))

    def completed(self, event):
        self_channel = Presence.objects.get(channel_name=self.channel_name)
        competitor = Room.objects.get(channel_name=self.room_group_name).presence_set.filter(~Q(channel_name=self_channel)).first().user
        if competitor.is_authenticated:
            competitor.won_games = competitor.won_games + 1
            competitor.save()
        user = self.scope['user']
        if user.is_authenticated:
            user.lost_games = user.lost_games + 1
            user.save()
    
    def draw(self, event):
        self_channel = Presence.objects.get(channel_name=self.channel_name)
        competitor = Room.objects.get(channel_name=self.room_group_name).presence_set.filter(~Q(channel_name=self_channel)).first().user
        if competitor.is_authenticated:
            competitor.draw_games += 1
            competitor.save()
        user = self.scope['user']
        if user.is_authenticated:
            user.draw_games += 1
            user.save() 

        

      