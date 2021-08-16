from django.urls import path
from .views import *

app_name = 'app'
urlpatterns = [
    path('', header, name='header'),
    path('home/', home, name='home'),
    path('bot/', bot, name='bot'),
    path('ai/', ai, name='ai'),
    path('leaderboard/', board, name='board'),
    path('local/', local, name='local'),
    path('online/', online, name='online'),
    path('notifications/', notifications, name='notifications'),
    path('game/', game, name='game'),
    path('about/', about, name='about'),
    path('new_game/', new_game, name='new_game'),
]