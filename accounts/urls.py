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
    path('logout/', LogoutView.as_view(next_page=conf.settings.LOGOUT_REDIRECT_URL), name='logout'),

]
