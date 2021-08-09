from django.shortcuts import render
from accounts.decorators import *
# Create your views here.
@restrict_unlogged(next='chat')
def chat(request):
    return render(request, 'chat/chat.html')