from django.urls import path
from chat.consumers import GlobalChatConsumer
from game.consumers import GameConsumer

websocket_urlpatterns = [
    path('ws/chat/', GlobalChatConsumer.as_asgi()),
    path('ws/game/<str:room>/', GameConsumer.as_asgi()),
]