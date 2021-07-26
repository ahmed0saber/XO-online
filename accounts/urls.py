from accounts.views import *
from django.urls import path

app_name = 'accounts'
urlpatterns = [
    path('signup/', sign_up, name='signup'),
    path('login/', log_in, name='login'),
    path('profile/', profile, name='profile'),
    path('settings/', settings, name='settings'),
]
