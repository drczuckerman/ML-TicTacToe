import player_types
from board import Board
from learning_computer_player import run_if_learner

class Game(object):
    def get_and_load_player(self, player_type, piece):
        player = player_types.get_player(player_type)
        run_if_learner(player, lambda: player.load(piece))
        return player

    def swap_players(self, player1, player2):
        run_if_learner(player1, lambda: player1.load(Board.O))
        run_if_learner(player2, lambda: player2.load(Board.X))
        return player2, player1
