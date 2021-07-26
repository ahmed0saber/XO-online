from django.shortcuts import render
from accounts.decorators import *
# Create your views here.
@restrict_unlogged
def chat(request):
    return render(request, 'chat/chat.html')