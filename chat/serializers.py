from .models import global_message
from accounts.models import CustomUser
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers


class messageSenderSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['front_id', 'image', 'first_name', 'last_name']

class messageSerializer(ModelSerializer):
    sender = messageSenderSerializer()
    
    class Meta:
        model = global_message
        fields = ['content', 'date_sent', 'unique_id', 'sender']
        
