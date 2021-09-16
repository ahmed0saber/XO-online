from django.contrib import admin
from channels_presence.models import Room
from .models import Match

# Register your models here.
admin.site.register(Room)
admin.site.register(Match)