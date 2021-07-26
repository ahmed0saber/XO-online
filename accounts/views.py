from django.shortcuts import render

# Create your views here.
def sign_up(request):
    return render(request, 'accounts/signup.html')

def log_in(request):
    return render(request, 'accounts/login.html')

def profile(request):
    return render(request, 'accounts/profile.html')

def settings(request):
    return render(request, 'accounts/settings.html')