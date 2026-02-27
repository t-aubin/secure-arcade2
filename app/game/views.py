import random

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, "home.html")

@login_required
def dashboard(request):
    return render(request, "dashboard.html")

from django.shortcuts import redirect
from django.contrib.auth import login
from .forms import RegisterForm

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("dashboard")
    else:
        form = RegisterForm()

    return render(request, "register.html", {"form": form})

from .models import Game
from django.shortcuts import get_object_or_404

@login_required
def new_game(request):
    game = Game.objects.create(
        player_x=request.user,
        player_o=None  # Computer
    )
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

    # Human can only move when it's X's turn
    if game.current_turn != "X":
        return redirect("game_detail", game_id=game.id)

    # ---- HUMAN MOVE ----
    board = list(game.board_state)
    board[position] = "X"
    game.board_state = "".join(board)

    if check_winner(game.board_state):
        game.winner = "X"
        game.is_active = False

        # Update stats
        request.user.wins += 1
        request.user.games_played += 1
        request.user.save()

    else:
        # ---- COMPUTER MOVE ----
        empty_positions = [i for i, v in enumerate(game.board_state) if v == "-"]

        if empty_positions:
            computer_move = random.choice(empty_positions)
            board = list(game.board_state)
            board[computer_move] = "O"
            game.board_state = "".join(board)

            if check_winner(game.board_state):
                game.winner = "O"
                game.is_active = False

                # Update stats
                request.user.losses += 1
                request.user.games_played += 1
                request.user.save()

    # ---- DRAW CHECK ----
    if "-" not in game.board_state and not game.winner:
        game.is_active = False

    game.save()

    return redirect("game_detail", game_id=game.id)

def check_winner(board):
    winning_positions = [
        (0,1,2), (3,4,5), (6,7,8),
        (0,3,6), (1,4,7), (2,5,8),
        (0,4,8), (2,4,6)
    ]

    for a, b, c in winning_positions:
        if board[a] == board[b] == board[c] and board[a] != "-":
            return True

    return False