import pickle
import os
from player import Player

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

    def _load_file(self, filenames):
        with open(self._get_filename(filenames), "rb") as f:
            contents = pickle.load(f)
            self.set_params(**contents["params"])
            return contents["learned"]

    def _get_filename(self, filenames):
        return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", filenames[self.piece]))

    def save(self):
        pass

    def _save_file(self, filenames, learned):
        with open(self._get_filename(filenames), "wb") as f:
            return pickle.dump({"learned": learned, "params": self.get_params()}, f)
