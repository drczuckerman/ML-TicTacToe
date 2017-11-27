import sys
import argparse
import textwrap
import pickle
import utils
import player_types
from game import Game
from game_controller import GameController
from board import Board
from random_player import RandomPlayer

class CompeteRandom(Game):
    def __init__(self, args):
        parsed_args = self._parse_args(args)
        self.num_games = parsed_args.num_games
        self.player1 = self.get_and_load_player(parsed_args.learning_type, Board.X)
        self.player2 = self.get_and_load_player(parsed_args.learning_type, Board.O)
        self.random_player = RandomPlayer()

    def _parse_args(self, args):
        parser = argparse.ArgumentParser(
            description="Compete Machine Learning against Random Tic-Tac-Toe Players",
            formatter_class=argparse.RawTextHelpFormatter,
            epilog=textwrap.dedent("where LEARNING_TYPE is as follows:\n" +
                                   player_types.get_learning_player_command_line_args()))
        parser.add_argument(
            "-g", "--num-games", default=20000, type=int, help="number of games to play")
        parser.add_argument(
            "-l", "--learning-type", choices=player_types.get_learning_player_types(),
            default="TD", dest="learning_type", metavar="LEARNING_TYPE")
        return parser.parse_args(args)

    def compete(self):
        results = {Board.X: self._init_results(), Board.O: self._init_results()}
        for game_number in range(self.num_games):
            self._show_progress(game_number+1)
            self._compete_and_update_results(self.player1, self.random_player, results[Board.X], Board.O)
            self._compete_and_update_results(self.random_player, self.player2, results[Board.O], Board.X)
        return results

    def _init_results(self):
        return {"num_losses": 0, "losing_moves": []}

    def _show_progress(self, game_number):
        if game_number % 1000 == 0:
            print("{} of {} games played".format(game_number, self.num_games))

    def _compete_and_update_results(self, player1, player2, results, opponent):
        winner, moves = self._compete_game(player1, player2)
        if winner == opponent:
            results["num_losses"] += 1
            if moves not in results["losing_moves"]:
                results["losing_moves"].append(moves)

    def _compete_game(self, player1, player2):
        controller = GameController(player1, player2)
        winner = None
        moves = []
        while winner is None:
            winner, move = controller.make_move()
            moves.append(move)
        return winner, moves

    def show_results(self, results):
        self._show_individual_results(results, Board.X)
        self._show_individual_results(results, Board.O)

    def _show_individual_results(self, results, piece):
        print("{} Results:".format(Board.format_piece(piece)))
        num_losses = results[piece]["num_losses"]
        print("- Losses: {} ({}%)".format(num_losses, 100.0*num_losses/self.num_games))

        losing_moves = sorted(results[piece]["losing_moves"])
        if losing_moves:
            print("- Losing moves:")
            for losing_moves in losing_moves:
                print("- - {}".format(", ".join(map(str, losing_moves))))

    def save_results(self, results):
        with open(utils.get_path("data", self.player1.__class__.__name__ + "LosingResults.pkl"), "wb") as f:
            pickle.dump(results, f)

def main(args=sys.argv[1:]):
    competer = CompeteRandom(args)
    results = competer.compete()
    competer.show_results(results)
    competer.save_results(results)

if __name__ == "__main__":
    sys.exit(main())

