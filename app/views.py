from django.shortcuts import render
from accounts.decorators import *
# Create your views here.
def header(request):
    return render(request, 'app/start.html')

def home(request):
    return render(request, 'app/newhome.html')

def bot(request):
    return render(request, 'app/easy_bot.html')

def ai(request):
    return render(request, 'app/ai_bot.html')

def notifications(request):
    return render(request, 'app/notifications.html')

def board(request):
    return render(request, 'app/leaderboard.html')

def local(request):
    return render(request, 'app/local.html')

@restrict_unlogged
def online(request):
    return render(request, 'app/online.html')

@restrict_unlogged
def game(request):
    return render(request, 'app/match_found.html')

def about(request):
    return render(request, 'app/newabout.html')