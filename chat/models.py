from django.db import models
from accounts.models import CustomUser
import uuid
# Create your models here.
class global_message(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date_sent = models.DateTimeField(auto_now_add=True)
    content =  models.TextField()
    unique_id = models.CharField(max_length=100, default=uuid.uuid4, unique=True)

    def __str__(self):
        return self.content[:20]