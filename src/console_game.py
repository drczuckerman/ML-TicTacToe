import sys
from board import Board
from game_controller import GameController
from computer_player import run_if_computer

class ConsoleGame(object):
    def play_one_game(self, player1, player2):
        self.controller = GameController(player1, player2)
        winner = None
        while winner is None:
            player = self.controller.get_player()
            self._show_turn(player)
            self._show_board()
            winner, position = self.controller.make_move()
            self._show_move(player, position)

        self._show_game_over(winner)
        return winner

    def _show_turn(self, player):
        piece = Board.format_piece(player.piece)
        print("It's your turn, {}".format(piece))

    def _show_board(self):
        print(self.controller.board.format_board(), end="")

    def _show_move(self, player, position):
        run_if_computer(player, lambda: print(player.indicate_move(position)))
        print()

    def _show_game_over(self, winner):
        print("Game over")
        self._show_board()
        print(self.controller.board.get_winner_text(winner))
        print()

def main(args=sys.argv[1:]):
    from random_player import RandomPlayer
    from td_learning_player import TDLearningPlayer
    
    console = ConsoleGame()
    player1 = TDLearningPlayer()
    player2 = TDLearningPlayer()
    random_player = RandomPlayer()
    player1.load(Board.X)
    player2.load(Board.O)
    num_games = 20000

    _compete(num_games, console, player1, player2)
    input("Self done. Press ENTER to continue...")

    _compete(num_games, console, player1, random_player)
    input("X vs random done. Press ENTER to continue...")

    _compete(num_games, console, random_player, player2)
    input("O vs random done. Press ENTER to continue...")

def _compete(num_games, console, player1, player2):
    stats = {Board.X: 0, Board.O: 0, Board.DRAW: 0}
    for n in range(num_games):
        print("Game #{}".format(n))
        winner = console.play_one_game(player1, player2)
        stats[winner] += 1
    print("X Losses={}%, O Losses={}%".format(
        100.0*stats[Board.O]/num_games, 100.0*stats[Board.X]/num_games))

if __name__ == "__main__":
    sys.exit(main())
