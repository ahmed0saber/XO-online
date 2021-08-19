from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from .models import CustomUser


@api_view(['GET'])
def check_email(request):
    mail = request.GET.get('email', None)
    try:
        validate_email(mail)
        query = CustomUser.objects.filter(email=mail)        
        if query.exists():
            return Response({"error":"This email already has account"}, status=status.HTTP_409_CONFLICT)
        else:
            return Response({"success":"This email is valid"}, status=status.HTTP_200_OK)
    except ValidationError as e:
        return Response({"error":"This email is invalid please enter a valid email address"}, status=status.HTTP_406_NOT_ACCEPTABLE)
