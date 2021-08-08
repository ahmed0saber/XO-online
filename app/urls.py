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
    path('game/', game, name='game'),
    path('about/', about, name='about'),
]