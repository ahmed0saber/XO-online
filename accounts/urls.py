from accounts.views import log_in, sign_up
from django.urls import path

app_name = 'accounts'
urlpatterns = [
    path('signup', sign_up, name='signup'),
    path('login', log_in, name='login')
]
