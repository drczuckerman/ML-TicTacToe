import random
from computer_player import ComputerPlayer
from board import Board

class TDLearningPlayer(ComputerPlayer):
    DEFAULT_ALPHA = 0.1
    DEFAULT_EPSILON = 0.1
    DEFAULT_X_DRAW_REWARD = 0.5
    DEFAULT_O_DRAW_REWARD = 0.5
    
    def __init__(self):
        super().__init__()
        self.values = {}
        self.reset()

    def set_params(self, **kwargs):
        super().set_params(**kwargs)
        self.alpha = kwargs.get("alpha", self.DEFAULT_ALPHA)
        self.epsilon = kwargs.get("epsilon", self.DEFAULT_EPSILON)
        self.draw_rewards = {Board.X: kwargs.get("x_draw_reward", self.DEFAULT_X_DRAW_REWARD),
                             Board.O: kwargs.get("o_draw_reward", self.DEFAULT_O_DRAW_REWARD)}

    def get_params(self):
        return \
        {
            "alpha": self.alpha,
            "epsilon": self.epsilon,
            "x_draw_reward": self.draw_rewards[Board.X],
            "o_draw_reward": self.draw_rewards[Board.O]
        }

    def store_state(self):
        self.states.append(tuple(self.board.state))
        
    def reset(self):
        super().reset()
        self.states = []

    def _get_reward(self, winner):
        if winner == Board.DRAW:
            return self.draw_rewards[self.piece]
        if winner == self.piece:
            return 1.0
        return 0.0

    def _get_value(self, state, winner=None):
        value = self.values.get(state)
        if value is None:
            value = 0.5 if winner is None else self._get_reward(winner)
            self.values[state] = value
        return value

    def set_reward(self, winner):
        if self.learning:
            last_value = self._get_value(self.states[-1], winner)
            for state in reversed(self.states[:-1]):
                current_value = self._get_value(state)
                current_value += self.alpha*(last_value - current_value)
                self.values[state] = current_value
                last_value = current_value

    def get_move(self):
        return self._choose_random_move() if self.learning and random.random() < self.epsilon \
            else self._choose_best_move()
        
    def _choose_random_move(self):
        return random.choice(self.board.get_available_moves())

    def _choose_best_move(self):
        max_value = -1
        best_moves = []
        for position in self.board.get_available_moves():
            with self.board.try_move(position, self.piece) as (winner, state):
                value = self._get_value(state, winner)
            if value > max_value:
                max_value = value
                best_moves = [position]
            elif value == max_value:
                best_moves.append(position)
        return random.choice(best_moves)

    def load(self):
        self.values = self._load_file()

    def save(self):
        self._save_file(self.values)
