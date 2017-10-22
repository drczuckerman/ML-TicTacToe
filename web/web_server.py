import os
import web_utils
import player_types
from bottle import get, post, run, static_file, request, response
from board import Board
from web_game import WebGame
from web_utils import get_template

@get('/')
def home():
    return get_template("home", player_types_dict=game.player_types_dict)

@post('/play')
def play():
    game.start_game(request.json)
    return get_template("play", game_info=game.start_game(request.json), player_types=request.json)

@get('/computer_move')
def get_computer_move():
    return get_template("board", game_info=game.get_computer_move())

@post('/human_move')
def set_human_move():
    return get_template("board", game_info=game.get_human_move(request.json["move"]))

@get('<path:path>')
def get_static(path):
    return static_file(path, root=web_utils.root)

@post('<path:path>')
def post_static(path):
    response.status = 404

game = WebGame()
run(host="0.0.0.0", port=8888)
