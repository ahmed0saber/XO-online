from django.urls import path
from django.urls.conf import include
from chat.consumers import GlobalChatConsumer

websocket_urlpatterns = [
    path('ws/chat/', GlobalChatConsumer.as_asgi()),
    # path('ws/game/', )
]