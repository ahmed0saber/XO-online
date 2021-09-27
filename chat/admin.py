from django.contrib.admin import ModelAdmin
from django.contrib import admin
from .models import global_message
# Register your models here.


class MessagesAdmin(ModelAdmin):
    list_display = ('content', 'id', 'sender', 'date_sent', 'unique_id')
    search_fields = ('content', 'unique_id')

admin.site.register(global_message, MessagesAdmin)
