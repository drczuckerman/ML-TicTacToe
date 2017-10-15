from board import Board

class Player(object):
    def __init__(self):
        self.board = None
        self.piece = None
        
    def get_move(self):
        pass
        
    def set_board(self, board):
        self.board = board
        
    def set_piece(self, piece):
        self.piece = piece
