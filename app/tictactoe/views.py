import random
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Game

@login_required
def new_game(request):
    game = Game.objects.create(player_x=request.user)
    return redirect("game_detail", game_id=game.id)

@login_required
def game_detail(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    board = list(game.board_state)

    return render(request, "game_detail.html", {
        "game": game,
        "board": board
    })

@login_required
def make_move(request, game_id, position):
    game = get_object_or_404(Game, id=game_id)

    if not game.is_active:
        return redirect("game_detail", game_id=game.id)

    if game.board_state[position] != "-":
        return redirect("game_detail", game_id=game.id)

    # Human move (X)
    board = list(game.board_state)
    board[position] = "X"
    game.board_state = "".join(board)

    if check_winner(game.board_state):
        game.winner = "X"
        game.is_active = False
        request.user.wins += 1
        request.user.games_played += 1
        request.user.save()
    else:
        # Computer move (O)
        empty_positions = [i for i, v in enumerate(game.board_state) if v == "-"]

        if empty_positions:
            computer_move = random.choice(empty_positions)
            board = list(game.board_state)
            board[computer_move] = "O"
            game.board_state = "".join(board)

            if check_winner(game.board_state):
                game.winner = "O"
                game.is_active = False
                request.user.losses += 1
                request.user.games_played += 1
                request.user.save()

    if "-" not in game.board_state and not game.winner:
        game.is_active = False
        request.user.games_played += 1
        request.user.save()

    game.save()
    return redirect("game_detail", game_id=game.id)


def check_winner(board):
    winning_positions = [
        (0,1,2), (3,4,5), (6,7,8),
        (0,3,6), (1,4,7), (2,5,8),
        (0,4,8), (2,4,6)
    ]

    for a,b,c in winning_positions:
        if board[a] == board[b] == board[c] and board[a] != "-":
            return True

    return False