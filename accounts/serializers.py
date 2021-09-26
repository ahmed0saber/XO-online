from rest_framework.serializers import ModelSerializer
from .models import Notification


class EnglishNotificationsSerializer(ModelSerializer):
    class Meta:
        model = Notification
        fields = ['content', 'url']

class ArabicNotificationsSerializer(ModelSerializer):
    class Meta:
        model = Notification
        fields = ['arabic', 'url']