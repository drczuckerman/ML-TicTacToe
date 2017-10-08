import random
from player import Player
from board import Board

class TDLearningPlayer(Player):
    def __init__(self):
        super().__init__()
        self.values = {}
        self.states = []

    def set_params(self, **kwargs):
        super().set_params(**kwargs)
        self.alpha = kwargs.get("alpha", 0.5)
        self.epsilon = kwargs.get("epsilon", 0.1)
        self.draw_rewards = {Board.X: kwargs.get("x_draw_reward", 0.5),
                             Board.O: kwargs.get("o_draw_reward", 0.5)}

    def store_state(self):
        self.states.append(tuple(self.board.state))

    def _get_reward(self, winner):
        if winner == Board.DRAW:
            return self.draw_rewards[self.piece]
        if winner == self.piece:
            return 1.0
        return 0.0

    def _get_value(self, state, winner):
        value = self.values.get(state)
        if value is None:
            value = 0.5 if winner is None else self._get_reward(winner)
            self.values[state] = value
        return value

    def set_reward(self, winner):
        last_value = self._get_reward(winner)
        for state in reversed(self.states):
            current_value = self._get_value(state, winner)
            current_value += self.alpha*(last_value - current_value)
            self.values[state] = current_value
            last_value = current_value
            winner = None

    def get_move(self):
        return self._choose_random_move() if random.random() < self.epsilon else self._choose_best_move()
        
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
