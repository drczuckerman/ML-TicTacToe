import os
import web_utils
from bottle import get, run, template, static_file
from board import Board

@get('/')
def select_players():
    return template(web_utils.get_template_path("select_player"))

@get('<path:path>')
def static(path):
    return static_file(path, root=web_utils.root)

run(host="0.0.0.0", port=8888)
