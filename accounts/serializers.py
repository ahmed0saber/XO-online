from rest_framework.serializers import ModelSerializer, DateTimeField
from .models import Notification


class EnglishNotificationsSerializer(ModelSerializer):
    time = DateTimeField(format=r'%Y/%m/%d, %I:%M %p')
    class Meta:
        model = Notification
        fields = ['content', 'url', 'time']

class ArabicNotificationsSerializer(ModelSerializer):
    time = DateTimeField(format=r'%Y/%m/%d, %I:%M %p')
    class Meta:
        model = Notification
        fields = ['arabic', 'url', 'time']