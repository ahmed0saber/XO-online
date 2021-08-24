from django.urls.conf import include
from accounts.views import *
from django.urls import path
from django.contrib.auth.views import LogoutView
from django import conf

app_name = 'accounts'
urlpatterns = [
    path('signup/<str:next>/', sign_up, name='signup'),
    path('login/<str:next>/', log_in, name='login'),
    path('profile/', profile, name='profile'),
    path('settings/', settings, name='settings'),
    path('avatars/', avatars, name='avatars'),
    path('logout/', LogoutView.as_view(next_page=conf.settings.LOGOUT_REDIRECT_URL), name='logout'),
    path('user/<str:id>/', view_profile, name='view_user'),
    path('api/', include('accounts.api_urls', namespace='api')),
]
