from django.shortcuts import render
from django.views.generic import ListView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import messageSerializer
from accounts.decorators import restrict_unlogged
from .models import global_message

# Create your views here.
@restrict_unlogged(next='chat')
def chat(request):
    count = global_message.objects.count()
    messages = global_message.objects.all()[count-15:count]
    context =  {'messages':messages}
    return render(request, 'chat/chat.html', context)

class ChatView(ListView):
    model = global_message
    template_name = 'chat/chat.html'
    context_object_name = 'messages'


@api_view(['GET'])
def older_messages(request):
    latest = global_message.objects.get(unique_id=request.GET.get('id'))
    first = global_message.objects.first()
    if latest == first: return Response(messageSerializer(many=True).data)
    offset = 16
    query = global_message.objects.filter(id__gt=latest.id-offset, id__lt=latest.id).order_by('-date_sent')
    while query.count() < 15 and first not in query:
        offset += 15
        query = global_message.objects.filter(id__gt=latest.id-offset, id__lt=latest.id).order_by('-date_sent')
    serializer = messageSerializer(query, many=True)
    return Response(serializer.data)
