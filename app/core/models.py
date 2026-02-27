from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    games_played = models.IntegerField(default=0)
    elo_rating = models.IntegerField(default=1000)

    def __str__(self):
        return self.username