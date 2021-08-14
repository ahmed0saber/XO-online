from .models import global_message
from accounts.models import CustomUser
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers


class messageSenderSerializer(ModelSerializer):
    full_name = serializers.StringRelatedField()
    class Meta:
        model = CustomUser
        fields = ['front_id', 'image', 'full_name']

class messageSerializer(ModelSerializer):
    sender = messageSenderSerializer()
    
    class Meta:
        model = global_message
        fields = ['content', 'date_sent', 'unique_id', 'sender']
        
