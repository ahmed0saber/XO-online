from django.urls import path
from .views import *
app_name = 'chat'

urlpatterns = [
    path('', chat, name='chat'),
    path('older/', older_messages, name='older_messages')
]