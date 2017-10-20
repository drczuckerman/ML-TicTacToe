import os
import web_utils
from bottle import get, run, template, static_file
from board import Board

@get('/')
def select_players():
    return template(web_utils.get_template_path("select_player"))

@get('/play')
def play():
    game_info = \
    {
        "winner": Board.O,
        "winning_positions": [2, 4, 6],
        "turn": Board.O,
        "board": [Board.X, Board.X, Board.O, 
                  Board.X, Board.O, Board.O,
                  Board.O, Board.X, Board.EMPTY]
    }
    return template(web_utils.get_template_path("play"), game_info=game_info)

@get('<path:path>')
def static(path):
    return static_file(path, root=web_utils.root)

run(host="0.0.0.0", port=8888)
