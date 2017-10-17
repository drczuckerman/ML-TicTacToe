import sys
import player_types
from board import Board
from game_controller import GameController
from computer_player import run_if_computer
from learning_computer_player import run_if_learner

class ConsoleGame(object):
    ACTION_QUIT = 1
    ACTION_SAME_PLAYERS_AND_PIECES = 2
    ACTION_SAME_PLAYERS_DIFF_PIECES = 3
    ACTION_DIFF_PLAYERS = 4

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

    def play(self):
        pass

    def _select_players(self):
        return self._select_player(Board.X), self._select_player(Board.O)

    def _select_player(self, piece):
        print("Select {} player:".format(Board.format_piece(piece)))
        descriptions = player_types.get_player_descriptions()
        for menu_num, description in enumerate(descriptions, start=1):
            print("{}: {}".format(menu_num, description))

        index = self._get_selection("Select player", len(descriptions)) - 1
        player_type = player_types.get_player_types()[index]
        player = player_types.get_player(player_type)
        run_if_learner(player, lambda: player.load(piece))
        return player

    def _get_selection(self, prompt, max_value):
        while True:
            try:
                selection = int(input(prompt + ": ").strip())
                if selection < 1 or selection > max_value:
                    raise ValueError()

                print()
                return selection

            except ValueError:
                print("Invalid selection")

    def _get_action(self):
        print("""\
Select action:
1) Quit
2) Same players and pieces
3) Same players and different pieces
4) Different players""")
        return self._get_selection("Select action", 4)

    def _swap_players(self, player1, player2):
        run_if_learner(player1, lambda: player1.load(Board.O))
        run_if_learner(player2, lambda: player2.load(Board.X))
        return player2, player1

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
