import sys
import player_types
from game import Game
from board import Board
from game_controller import GameController
from computer_player import run_if_computer
from learning_computer_player import run_if_learner

class ConsoleGame(Game):
    ACTION_SAME_PLAYERS_AND_PIECES = 1
    ACTION_SAME_PLAYERS_DIFF_PIECES = 2
    ACTION_DIFF_PLAYERS = 3
    ACTION_QUIT = 4

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
        print(Board.get_winner_text(winner))
        print()

    def play(self):
        action = self.ACTION_DIFF_PLAYERS
        while action != self.ACTION_QUIT:
            if action == self.ACTION_DIFF_PLAYERS:
                player1, player2 = self._select_players()
            elif action == self.ACTION_SAME_PLAYERS_DIFF_PIECES:
                player1, player2 = self._swap_players(player1, player2)
            self.play_one_game(player1, player2)
            action = self._get_action()

    def _select_players(self):
        return self._select_player(Board.X), self._select_player(Board.O)

    def _select_player(self, piece):
        print("Select {} player:".format(Board.format_piece(piece)))
        descriptions = player_types.get_player_descriptions()
        for menu_num, description in enumerate(descriptions, start=1):
            print("{}) {}".format(menu_num, description))

        index = self._get_selection("Select player", len(descriptions)) - 1
        player_type = player_types.get_player_types()[index]
        return self.get_and_load_player(player_type, piece)

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
1) Same players and pieces
2) Same players and different pieces
3) Different players
4) Quit""")
        return self._get_selection("Select action", 4)

def main(args=sys.argv[1:]):
    console = ConsoleGame()
    console.play()
    return 0

if __name__ == "__main__":
    sys.exit(main())
