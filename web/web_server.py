import os
import web_utils
import player_types
from bottle import get, run, template, static_file
from board import Board
from game_controller import GameController
from computer_player import run_if_computer

def get_and_load_players(player_type, piece):
    player = player_types.get_player(player_type)
    run_if_computer(player, lambda: player.load(piece))

def get_game_info(controller):
    return \
    {
        "winner": controller.board.get_winner(),
        "winning_positions": controller.board.get_winning_positions(),
        "turn": controller.board.get_player().piece,
        "board": controller.board.state
    }
   
@get('/')
def select_players():
    return template(web_utils.get_template_path("select_player"))

@post('/play')
def play():
    global controller
    player1 = get_and_load_player(request.json["x"], Board.X)
    player2 = get_and_load_player(request.json["o"], Board.O)
    controller = GameController(player1, player2)
    return template(web_utils.get_template_path("play"), game_info=get_game_info())

@get('<path:path>')
def static(path):
    return static_file(path, root=web_utils.root)

controller = None
run(host="0.0.0.0", port=8888)
