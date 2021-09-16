from django.db.models.query_utils import Q
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.shortcuts import get_object_or_404
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser
from accounts.decorators import *
from game.models import Match

# Create your views here.
@restrict_logged
def sign_up(request, next):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            user = authenticate(request, email=email, password=password)
            if user:
                login(request, user)
                pathes = {
                    'profile':'accounts:profile',
                    'chat':'chat:chat',
                    'settings':'accounts:settings',
                    'game':'app:game',
                    'online':'app:online',
                    'notifications':'app:notifications',
                    'new_game':'app:new_game',
                    'avatars':'accounts:avatars'
                }
                return redirect(pathes.get(next, 'app:home'))
    else:
        form = CustomUserCreationForm()
    context = {
        'form':form,
        'next':next,
    }
    return render(request, 'accounts/signup.html', context)

@restrict_logged
def log_in(request, next):
    if request.method == 'POST':
        user = authenticate(request, email=request.POST.get('email'), password=request.POST.get('password'))
        if user:
            login(request, user)
            pathes = {
                    'profile':'accounts:profile',
                    'chat':'chat:chat',
                    'settings':'accounts:settings',
                    'game':'app:game',
                    'online':'app:online',
                    'notifications':'app:notifications',
                    'new_game':'app:new_game',
                    'avatars':'accounts:avatars'
                }
            return redirect(pathes.get(next, 'app:home'))
        else:
            messages.error(request, 'Wrong user name or password please check your info')
    
    return render(request, 'accounts/login.html', {'next':next})

@restrict_unlogged(next='profile')
def profile(request):
    try:
        rate = round(request.user.won_games/ request.user.total_games, 3) * 100 
    except ZeroDivisionError:
        rate = 0

    history = Match.objects.filter(Q(winner=request.user)|Q(loser=request.user)) | request.user.matches.all()
    history = history.order_by('-time')
    context =  {
        'win_rate': rate,
        'history': history
    }
    return render(request, 'accounts/profile.html', context)

@restrict_unlogged(next='settings')
def settings(request):
    if request.method == "POST":
        form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('accounts:profile')
    return render(request, 'accounts/settings.html')

@restrict_unlogged(next='avatars')
def avatars(request):
    if request.method == 'POST':
        choice = int(request.POST.get('choice'))
        if choice in range(1, 5):
            user = request.user
            user.image = f'images/{choice}.png'
            user.save()
            return redirect('accounts:profile')
        else:
            return redirect('accounts:profile')
    return render(request, 'accounts/avatars.html')



def view_profile(request, id):
    user = get_object_or_404(CustomUser, front_id=id)
    if user == request.user:
        return redirect('accounts:profile')
    if user.total_games == 0:
        rate = 0
    else:
        rate = round(user.won_games/ user.total_games, 3) * 100 
    return render(request, 'accounts/view_profile.html', {'friend':user, 'win_rate':rate})
