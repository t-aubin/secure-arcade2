from django.db import models
from django.conf import settings

class Game(models.Model):
    player_x = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="ttt_games_as_x"
    )
    player_o = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="ttt_games_as_o",
        null=True,
        blank=True
    )

    board_state = models.CharField(max_length=9, default="---------")
    winner = models.CharField(max_length=1, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"TicTacToe Game {self.id}"