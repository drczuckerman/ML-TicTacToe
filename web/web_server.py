from bottle import get, post, run, static_file, request, response
from web_game_manager import WebGameManager, start_web_game_manager_thread
from web_utils import get_template, root

@get('/')
def home():
    return get_template("home")

@post('/play')
def play():
    game_id, game = manager.new_game()
    return get_template(
        "play", game_info=game.start_game(request.json), player_types=request.json, game_id=game_id)

@post('/computer_move')
def computer_move():
    return make_move(request.json["game_id"], lambda game: game.make_computer_move())

@post('/human_move')
def human_move():
    return make_move(request.json["game_id"], lambda game: game.make_human_move(request.json["move"]))

def make_move(game_id, move_func):
    game = manager.get_game(game_id)
    if game is None:
        return get_template("expired")

    manager.refresh_game(game_id)
    game_info = move_func(game)
    if game_info["winner"] is not None:
        manager.delete_game(game_id)

    return get_template("board", game_info=game_info)

@get('<path:path>')
def get_static(path):
    return static_file(path, root=root)

@post('<path:path>')
def post_static(path):
    response.status = 404

manager = WebGameManager()
start_web_game_manager_thread(manager)
run(host="0.0.0.0", port=8888)

