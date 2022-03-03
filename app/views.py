from django.shortcuts import render
from accounts.decorators import *
from accounts.models import CustomUser
# Create your views here.
def header(request):
    return render(request, 'app/start.html')

def home(request):
    return render(request, 'app/start.html')

def single(request):
    return render(request, 'app/single.html')

def two(request):
    return render(request, 'app/two.html')

def bot(request):
    return render(request, 'app/easy_bot.html')

def ai(request):
    return render(request, 'app/ai_bot.html')

@restrict_unlogged(next='notifications')
def notifications(request):
    qs = request.user.notification.all().order_by('-id')
    return render(request, 'app/notifications.html', {'notifications': qs})

def board(request):
    winners = CustomUser.objects.all().order_by('-won_games')
    return render(request, 'app/leaderboard.html', {'users': winners})

def local(request):
    return render(request, 'app/local.html')

@restrict_unlogged(next='online')
def online(request):
    return render(request, 'app/online.html')


def new_game(request):
    return render(request, 'app/new_game.html')


def game(request):
    return render(request, 'app/match_found.html')

def about(request):
    return render(request, 'app/newabout.html')

    
