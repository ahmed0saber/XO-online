from .api_views import *
from django.urls import path

app_name = 'api'
urlpatterns = [
    path('check_email/', check_email, name='check_email'),
    path('check_password/', check_password, name='check_password'),
]