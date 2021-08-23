from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse
from django.core.files.base import ContentFile
from .managers import Manager

from PIL import Image
import uuid
from io import BytesIO
from PIL import ExifTags

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

    def win(self):
        self.won_games += 1
        self.save() 

    def lose(self):
        self.lost_games += 1
        self.save() 

    def draw(self):
        self.draw_games += 1
        self.save() 

    def compress(self, im:Image):
        ratio = im.height / im.width
        height = 256
        width = round(height / ratio)
        # create a BytesIO object
        im_io = BytesIO() 
        # save image to BytesIO object
        for orientation in ExifTags.TAGS.keys() : 
            if ExifTags.TAGS[orientation]=='Orientation' : break 
        exif=dict(im._getexif().items())

        if exif[orientation] == 3 : 
            im=im.rotate(180, expand=True)
        elif exif[orientation] == 6 : 
            im=im.rotate(270, expand=True)
        elif exif[orientation] == 8 : 
            im=im.rotate(90, expand=True)

        im.thumbnail([height,width], Image.ANTIALIAS)
        im = im.convert("RGB")
        im = im.save(im_io,'JPEG', quality=70) 
        # create a django-friendly Files object
        new_image = ContentFile(im_io.getvalue(), name=self.name+"ProfilePic.jpeg")
        return new_image

    def save(self, *args, **kwargs):

        image = Image.open(self.image)
        print(type(image))
        if image.height > 256:
            image = self.compress(image)
            self.image = image

        super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    