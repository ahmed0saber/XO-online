from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from channels_presence.models import Room

# Create your views here.
@api_view(['GET'])
def check_room(request):
    target =  request.GET.get('room')
    if target is None:
        return Response({"error":"Please identify a room name to check"}, status=status.HTTP_400_BAD_REQUEST)
    room = Room.objects.filter(channel_name='game_'+target)
    if not room.exists():
        return Response({"error":"Couldn't find this room please check your code"}, status=status.HTTP_404_NOT_FOUND)

    if room.first().presence_set.count() < 1:
        return Response({"error":"This room is full please try another room"}, status=status.HTTP_400_BAD_REQUEST)
    return Response({"message":"This room is available"}, status=status.HTTP_200_OK)


