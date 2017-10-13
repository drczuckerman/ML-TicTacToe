import pickle
import os
import utils
from player import Player
from board import Board

class ComputerPlayer(Player):
    def __init__(self):
        super().__init__()
        self.set_params()
        self.disable_learning()

    def set_params(self, **kwargs):
        pass

    def get_params(self):
        return {}

    def store_state(self):
        pass
        
    def set_reward(self, winner):
        pass

    def disable_learning(self):
        self.learning = False

    def enable_learning(self):
        self.learning = True

    def load(self):
        pass

    def _load_file(self):
        with open(self._get_filename(), "rb") as f:
            contents = pickle.load(f)
            self.set_params(**contents["params"])
            return contents["learned"]

    def _get_filename(self):
        filename = self.__class__.__name__ + Board.format_piece(self.piece) + ".pkl"
        return utils.get_path("data", filename)

    def save(self):
        pass

    def _save_file(self, learned):
        with open(self._get_filename(), "wb") as f:
            return pickle.dump({"learned": learned, "params": self.get_params()}, f)
