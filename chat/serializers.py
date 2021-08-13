from django.db import models
from django.db.models import fields
from .models import global_message
from rest_framework.serializers import ModelSerializer

class messageSerializer(ModelSerializer):
    class Meta:
        model = global_message
        fields = ['sender', 'content', 'date_sent', 'unique_id']