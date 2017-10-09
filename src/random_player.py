import random
from computer_player import ComputerPlayer

class RandomPlayer(ComputerPlayer):
    def get_move(self):
        return random.choice(self.board.get_available_moves())
