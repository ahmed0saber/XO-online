from django.db import models
from accounts.models import CustomUser
# Create your models here.
class Match(models.Model):
    winner = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, blank=True, null=True, related_name='won_matches')
    loser = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, blank=True, null=True, related_name='lost_matches')
    draw = models.ManyToManyField(CustomUser, blank=True, related_name='matches')
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        winner = loser = 'Unknwon User'
        if self.winner or self.loser:
            return f'A match between {self.winner.name if self.winner else winner} and {self.loser.name if self.loser else loser}'
        return f'a draw game between {" ".join(map(str, self.draw.all()))}'
