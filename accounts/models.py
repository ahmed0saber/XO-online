from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _

from .managers import Manager

import uuid
# Create your models here.

class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    front_id = models.UUIDField(default=uuid.uuid4, editable=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = Manager()

    def __str__(self):
        return self.email
    