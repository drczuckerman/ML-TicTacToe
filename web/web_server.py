import os
import web_utils
import player_types
from bottle import get, post, run, template, static_file, request
from board import Board
from game_controller import GameController
from learning_computer_player import run_if_learner
from human_player import run_if_human

def get_and_load_player(player_type, piece):
    player = player_types.get_player(player_type)
    run_if_learner(player, lambda: player.load(piece))
    run_if_human(player, lambda: player.set_non_interactive())
    return player

def get_game_info(controller):
    return \
    {
        "winner": controller.board.get_winner(),
        "winning_positions": controller.board.get_winning_positions(),
        "turn": controller.get_player().piece,
        "board": controller.board.state
    }

@get('/')
def select_players():
    return template(web_utils.get_template_path("select_players"))

@post('/play')
def play():
    global controller
    player1 = get_and_load_player(request.forms["x"], Board.X)
    player2 = get_and_load_player(request.forms["o"], Board.O)
    controller = GameController(player1, player2)
    return template(
        web_utils.get_template_path("play"), game_info=get_game_info(controller), player_types=request.forms)

@get('/computer_move')
def get_computer_move():
    controller.make_move()
    return template(web_utils.get_template_path("board"), game_info=get_game_info(controller))

@post('/human_move')
def set_human_move():
    player = controller.get_player()
    player.set_move(int(request.json["move"]))
    return template(web_utils.get_template_path("board"), game_info=get_game_info(controller))

@get('<path:path>')
def static(path):
    return static_file(path, root=web_utils.root)

controller = None
run(host="0.0.0.0", port=8888)
