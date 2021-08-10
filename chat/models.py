from django.db import models
from accounts.models import CustomUser

# Create your models here.
class global_message(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date_sent = models.DateTimeField(auto_now_add=True)
    content =  models.TextField()

    def __str__(self):
        return self.content[:20]