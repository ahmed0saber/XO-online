from asgiref.sync import async_to_sync
import channels
from channels.generic.websocket import WebsocketConsumer
from channels_presence.models import Room, Presence

from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from accounts.models import CustomUser, Notification
from chat.serializers import messageSenderSerializer
import json
import string 
import random
import logging

db_logger = logging.getLogger('db')

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
                'room':self.room_name,
            }))

            connected_count = 0
        elif self.room_name == 'random':
            counter = 1
            while self.room_name == 'random':
                try:
                    room:Room = Room.objects.get(channel_name=f'random_{counter}')
                except ObjectDoesNotExist as e:
                    room = Room.objects.create(channel_name=f'random_{counter}')
                connected_count = room.presence_set.count()
                if connected_count < 2:
                    self.room_name = f'random_{counter}'
                    self.room_group_name = f'random_{counter}'
                    if connected_count == 0:
                        self.send(json.dumps({
                            'type':'created',
                            'room':self.room_name,
                        }))
                counter += 1
                
        elif self.room_name == 'invite':
            try:
                invited = self.scope['url_route']['kwargs']['invited']
                invited = CustomUser.objects.get(front_id=invited)
            except Exception as e:
                print(e)
                self.send(json.dumps({
                    'type':'error',
                    'code':'404',
                    'error':'Can\'t find the user'
                }))
                self.close()
            else:
                all = string.digits + string.ascii_letters
                name = random.choices(all, k=16)
                self.room_name = "".join(name)
                self.room_group_name = 'game_' + self.room_name
                notifi = Notification.objects.create(user=invited, invitor=self.scope['user'], room=self.room_name)
                notifi.save()
                self.send(json.dumps({
                    'type':'invited',
                    'friend':invited.name,
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
                user = player.first().user  
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
                Room.objects.remove(self.room_group_name, self.channel_name)
        except Exception as e:
            print('error occured')
            print(e)
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
        if text_data['type'] ==  'completed':
            
            user:CustomUser = self.scope['user']
            if user.is_authenticated:
                user = CustomUser.objects.get(id=user.id)
                user.lost_games += 1
                user.save()

            competitor:CustomUser = Room.objects.get(channel_name=self.room_group_name).presence_set.filter(~Q(channel_name=self.channel_name)).first().user
            if competitor:
                competitor.won_games += 1
                competitor.save()
            return 
        elif text_data['type'] == 'draw':
            competitor:CustomUser = Room.objects.get(channel_name=self.room_group_name).presence_set.filter(~Q(channel_name=self.channel_name)).first().user
            if competitor:
                competitor.draw_games += 1
                competitor.save()
            user = self.scope['user']
            if user.is_authenticated:
                user = CustomUser.objects.get(id=user.id)
                user.draw_games += 1
                user.save()           
            return


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
            try:
                event.update({
                    'self': {
                        'front_id':None,
                        'image':CustomUser().image.url,
                        'name':'Unknown User',
                        'profile_url':"#"
                    }
                })
            except Exception as e:
                print('cannot complete room')
                print(e)

        if competitor:
            serializer = messageSenderSerializer(instance=competitor)
            event.update({
                'competitor': serializer.data
            })
        else:
            try:
                event.update({
                    'competitor': {
                        'front_id':None,
                        'image':CustomUser().image.url,
                        'name':'Unknown User',
                        'profile_url':"#"
                    }
                })
            except Exception as e:
                print('cannot complete room')
                print(e)

        self.send(json.dumps(event))
    
    def restart(self, event):
        self.send(json.dumps(event))

