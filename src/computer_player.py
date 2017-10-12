import pickle
import os
from player import Player

class ComputerPlayer(Player):
    def __init__(self):
        super().__init__()
        self.disable_learning()

    def set_params(self, **kwargs):
        pass

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

    def _load_file(self, filenames):
        with open(self._get_filename(filenames), "r") as f:
            return pickle.load(f)

    def _get_filename(self, filenames):
        return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", filenames[self.piece]))

    def save(self):
        pass

    def _save_file(self, filenames, values):
        with open(self._get_filename(filenames), "w") as f:
            return pickle.dump(values, f)
