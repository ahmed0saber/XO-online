from .models import global_message
from accounts.models import CustomUser
import random 
import string

users = CustomUser.objects.all()
for i in range(100):
    user = random.choice(users)
    content = "".join(random.choices(string.ascii_letters, k=random.randint(20, 100)))
    new_message = global_message.objects.create(sender=user, content=content)
    new_message.save()
