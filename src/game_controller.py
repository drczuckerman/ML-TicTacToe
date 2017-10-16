from board import Board
from learning_computer_player import LearningComputerPlayer, run_if_learner

class GameController(object):
    def __init__(self, x_player, o_player):
        self.players = [x_player, o_player]
        self.board = Board()
        self.player_number = 0
        for player, piece in zip(self.players, [Board.X, Board.O]):
            run_if_learner(player, lambda: player.reset())
            player.set_board(self.board)
            player.set_piece(piece)
            
    def get_player(self):
        return self.players[self.player_number]
            
    def make_move(self):
        player = self.get_player()
        position = player.get_move()
        self.board.make_move(position, player.piece)
        self.player_number = 1 - self.player_number
        return self.board.get_winner(), position
