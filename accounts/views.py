from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import login, authenticate
from .forms import CustomUserCreationForm, CustomUserChangeForm
from accounts.decorators import *

# Create your views here.
@restrict_logged
def sign_up(request):
    form = CustomUserCreationForm()
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            user = authenticate(request, email=email, password=password)
            if user:
                login(request, user)
                return redirect('app:online')

    return render(request, 'accounts/signup.html', {'form':form})

@restrict_logged
def log_in(request):
    if request.method == 'POST':
        user = authenticate(request, email=request.POST.get('email'), password=request.POST.get('password'))
        if user:
            login(request, user)
            return redirect('app:online')
        else:
            messages.error(request, 'Wrong user name or password please check your info')
    return render(request, 'accounts/login.html')

@restrict_unlogged
def profile(request):
    if request.user.total_games != 0:
        rate = request.user.won_games / request.user.total_games
    else:
        rate = 0
    return render(request, 'accounts/profile.html', {'win_rate': rate})

@restrict_unlogged
def settings(request):
    if request.method == "POST":
        form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            user = form.save()
            print(type(request.POST.get('image')))
            # user.image = request.POST.get('image')
            # user.save()
            return redirect('accounts:profile')
    return render(request, 'accounts/settings.html')