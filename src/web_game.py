import player_types
from game import Game
from board import Board
from game_controller import GameController
from human_player import run_if_human

class WebGame(Game):
    def __init__(self):
        self.controller = None
        self.player1 = None
        self.player2 = None
        self.player_types_dict = {Board.X: "", Board.O: ""}

    def start_game(self, player_types_dict):
        self.player1 = self.get_and_load_player(self.player1, player_types_dict["x"], Board.X)
        self.player2 = self.get_and_load_player(self.player2, player_types_dict["o"], Board.O)
        self.controller = GameController(self.player1, self.player2)
        return self._get_game_info(None)

    def _get_game_info(self, winner):
        return \
        {
            "winner": winner,
            "winning_positions": self.controller.board.get_winning_positions(),
            "turn": self.controller.get_player().piece,
            "board": self.controller.board.state
        }

    def get_and_load_player(self, player, player_type, piece):
        if self.player_types_dict[piece] != player_type:
            player = super().get_and_load_player(player_type, piece)
            run_if_human(player, lambda: player.set_non_interactive())
            self.player_types_dict[piece] = player_type
        return player

    def make_computer_move(self):
        return self._make_move()

    def _make_move(self):
        winner, _ = self.controller.make_move()
        return self._get_game_info(winner)

    def make_human_move(self, position):
        player = self.controller.get_player()
        player.set_move(int(position.strip()))
        return self._make_move()
