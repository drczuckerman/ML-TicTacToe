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
    
    stats = {Board.X: 0, Board.O: 0, Board.DRAW: 0}
    console = ConsoleGame()
    player1 = TDLearningPlayer()
    player2 = TDLearningPlayer()
    random_player = RandomPlayer()
    player1.enable_learning()
    player2.enable_learning()
    num_games = 20000
    for n in range(num_games):
        print("Game #{}".format(n))
        winner = console.play_one_game(player1, player2)
        player1.store_state()
        player2.store_state()
        player1.set_reward(winner)
        player2.set_reward(winner)
        stats[winner] += 1
    print("X Losses={}%, O Losses={}%".format(
        100.0*stats[Board.O]/num_games, 100.0*stats[Board.X]/num_games))
    input("Training done. Press ENTER to continue...")
    player1.disable_learning()
    player2.disable_learning()
    
    stats = {Board.X: 0, Board.O: 0, Board.DRAW: 0}
    for n in range(num_games):
        print("Game #{}".format(n))
        winner = console.play_one_game(player1, player2)
        stats[winner] += 1
    print("X Losses={}%, O Losses={}%".format(
        100.0*stats[Board.O]/num_games, 100.0*stats[Board.X]/num_games))
    input("Self play done. Press ENTER to continue...")
    
    stats = {Board.X: 0, Board.O: 0, Board.DRAW: 0}
    for n in range(num_games):
        print("Game #{}".format(n))
        winner = console.play_one_game(player1, random_player)
        stats[winner] += 1
    print("X Losses={}%, O Losses={}%".format(
        100.0*stats[Board.O]/num_games, 100.0*stats[Board.X]/num_games))
    input("X vs random done. Press ENTER to continue...")
    
    stats = {Board.X: 0, Board.O: 0, Board.DRAW: 0}
    for n in range(num_games):
        print("Game #{}".format(n))
        winner = console.play_one_game(random_player, player2)
        stats[winner] += 1
    print("X Losses={}%, O Losses={}%".format(
        100.0*stats[Board.O]/num_games, 100.0*stats[Board.X]/num_games))
    input("O vs random done. Press ENTER to continue...")

if __name__ == "__main__":
    sys.exit(main())
