from td_learning_player import TDLearningPlayer
from symmetry import Symmetry

class TDSymmetricLearningPlayer(TDLearningPlayer):
    def _find_value_and_state(self, state, winner=None):
        for symmetric_state in Symmetry().get_symmetries(state):
            value = self.values.get(symmetric_state)
            if value is not None:
                state = symmetric_state
                break

        return value, state
