from os import name
from django.urls import path
from django.views.generic.base import TemplateView
from .views import *
from game.views import check_room
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
    path('game/check_room/', check_room, name='check_room'),
    path('about/', about, name='about'),
    path('new_game/', new_game, name='new_game'),
    path('manifest.js', TemplateView.as_view(template_name='app/manifest.webmanifest', content_type='application/x-javascript'), name='manifest'),
    path('sw.js', TemplateView.as_view(template_name='app/sw.js', content_type='application/x-javascript'), name='worker'),
]