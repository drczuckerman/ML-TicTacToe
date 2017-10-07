from board import Board

class Player(object):
    def __init__(self):
        self.board = None
        self.piece = None
        
    def set_board(self, board):
        self.board = board
        
    def set_piece(self, piece):
        self.piece = piece

    def set_params(self, **kwargs):
        pass

    def store_state(self):
        pass

    def set_reward(self, winner):
        pass
