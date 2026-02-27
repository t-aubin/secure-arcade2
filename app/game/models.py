from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    games_played = models.IntegerField(default=0)
    elo_rating = models.IntegerField(default=1000)

    def __str__(self):
        return self.username


class Game(models.Model):
    player_x = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="games_as_x"
    )
    player_o = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="games_as_o",
        null=True,
        blank=True
    )

    board_state = models.CharField(max_length=9, default="---------")
    current_turn = models.CharField(max_length=1, default="X")
    winner = models.CharField(max_length=1, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Game {self.id}"