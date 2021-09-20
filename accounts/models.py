from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse
from django.core.files.base import ContentFile
from .managers import Manager

import uuid
from PIL import Image
from io import BytesIO
from PIL.ImageOps import exif_transpose

# Create your models here.

class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    front_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    won_games = models.IntegerField(default=0)
    lost_games = models.IntegerField(default=0)
    draw_games = models.IntegerField(default=0)
    image = models.ImageField(default='images/default.png', upload_to='images')
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = Manager()

    @property
    def total_games(self):
        return self.won_games + self.lost_games + self.draw_games

    @property
    def name(self):
        return self.__str__()

    @property
    def profile_url(self):
        return reverse('accounts:view_user', kwargs={"id":self.front_id})


    def compress(self, im:Image):
        ratio = im.height / im.width
        height = 100
        width = round(height / ratio)
        # create a BytesIO object
        im_io = BytesIO() 
        # save image to BytesIO object
        im = exif_transpose(im)

        im = im.resize([height,width], Image.ANTIALIAS)
        
        im = im.convert("RGB")
        im = im.save(im_io,'JPEG', quality=70) 
        # create a django-friendly Files object
        im = ContentFile(im_io.getvalue(), name=self.name+"ProfilePic.jpeg")
        return  im

    def save(self, *args, **kwargs):

        image = Image.open(self.image)
        if image.height > 100:
            image = self.compress(image)
            self.image = image
        super(AbstractUser, self).save(*args, **kwargs)


    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    

class Notification(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='notification')
    invitor = models.ForeignKey(CustomUser, null=True, blank=True, on_delete=models.CASCADE, related_name='invitation')
    room = models.CharField(max_length=16)
    time = models.DateTimeField(auto_now_add=True)

    @property
    def content(self):
        if self.invitor:
            return f'Your friend {self.invitor.name} challenged you to play together click to play now !\nThis invitation is valid for 1 minute'
        else:
            return f'A friend challenged you to play together click to play now !\nThis invitation is valid for 1 minute'
    
    @property
    def url(self):
        return reverse('app:game') + f'?room={self.room}'