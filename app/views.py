from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'app/start.html')

def bot(request):
    return render(request, 'app/easy_bot.html')

def ai(request):
    return render(request, 'app/ai_bot.html')

def board(request):
    return render(request, 'app/leaderboard.html')

def local(request):
    return render(request, 'app/local.html')

def online(request):
    return render(request, 'app/online.html')

def game(request):
    return render(request, 'app/match_found.html')

def about(request):
    return render(request, 'app/about.html')