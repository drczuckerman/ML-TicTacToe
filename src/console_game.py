import sys
from board import Board
from game_controller import GameController

class ConsoleGame(object):
    def play_one_game(self, player1, player2):
        self.controller = GameController(player1, player2)
        winner = None
        while winner is None:
            player = self.controller.get_player()
            self._show_turn(player)
            self._show_board()
            winner = self.controller.make_move()
            print()

        self._show_game_over(winner)
        return winner

    def _show_turn(self, player):
        piece = Board.format_piece(player.piece)
        print("It's your turn, {}".format(piece))

    def _show_board(self):
        print(self.controller.board.format_board(), end="")

    def _show_game_over(self, winner):
        print("Game over")
        self._show_board()
        print(self.controller.board.get_winner_text(winner))

def main(args=sys.argv[1:]):
    from human_player import HumanPlayer
    console = ConsoleGame()
    player1 = HumanPlayer()
    player2 = HumanPlayer()
    console.play_one_game(player1, player2)

if __name__ == "__main__":
    sys.exit(main())
