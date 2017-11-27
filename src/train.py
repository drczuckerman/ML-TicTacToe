import sys
import argparse
import textwrap
import pickle
import utils
import player_types
from board import Board
from learning_computer_player import run_if_learner
from random_player import RandomPlayer
from game_controller import GameController

class Trainer(object):
    def __init__(self, args):
        parsed_args = self._parse_args(args)
        self.num_games = parsed_args.num_games
        self.num_batches = parsed_args.num_batches
        self.player1 = self._init_player(parsed_args)
        self.player2 = self._init_player(parsed_args)
        self.random_player = RandomPlayer()
        
    def _parse_args(self, args):
        parser = argparse.ArgumentParser(
            description="Train Machine Learning Tic-Tac-Toe Players",
            formatter_class=argparse.RawTextHelpFormatter,
            epilog=textwrap.dedent("where LEARNING_TYPE is as follows:\n" +
                                   player_types.get_learning_player_command_line_args()))
        parser.add_argument(
            "-g", "--num-games", default=20000, type=int, help="number of games to play")
        parser.add_argument(
            "-b", "--num-batches", default=1000, type=int, help="number of batches to gather stats")
        parser.add_argument(
            "-l", "--learning-type", choices=player_types.get_learning_player_types(),
            default="TD", dest="learning_type", metavar="LEARNING_TYPE")
        parser.add_argument("-a", "--alpha", type=float, help="learning rate")
        parser.add_argument("-e", "--epsilon", type=float, help="exploration rate")
        parser.add_argument("-x", "--x-draw-reward", type=float, help="X draw reward")
        parser.add_argument("-o", "--o-draw", type=float, help="O draw reward")
        return parser.parse_args(args)

    def _init_player(self, parsed_args):
        player = player_types.get_learning_player(parsed_args.learning_type)
        params = {key: value for key, value in parsed_args.__dict__.items() if value is not None}
        player.set_params(**params)
        return player

    def train(self):
        stats = \
        {
            "train_self": [], "train_x_vs_random": [], "train_o_vs_random": [],
            "compete_self": [], "compete_x_vs_random": [], "compete_o_vs_random": []
        }
        for game_number in range(0, self.num_games, self.num_batches):
            self._show_game_numbers(game_number)
            stats["train_self"].append(self._train_batch(self.player1, self.player2, "Train self"))
            stats["train_x_vs_random"].append(
                self._train_batch(self.player1, self.random_player, "Train X vs. random"))
            stats["train_o_vs_random"].append(
                self._train_batch(self.random_player, self.player2, "Train O vs. random"))
            stats["compete_self"].append(self._compete_batch(self.player1, self.player2, "Compete self"))
            stats["compete_x_vs_random"].append(
                self._compete_batch(self.player1, self.random_player, "Compete X vs. Random"))
            stats["compete_o_vs_random"].append(
                self._compete_batch(self.random_player, self.player2, "Compete O vs. Random"))

        return stats

    def _show_game_numbers(self, game_number):
        print("Game #{}-{}:".format(game_number+1, game_number+self.num_batches))

    def _train_batch(self, player1, player2, stat_type):
        run_if_learner(self.player1, lambda: self.player1.enable_learning())
        run_if_learner(self.player2, lambda: self.player2.enable_learning())

        stats = self._init_stats()
        for batch_number in range(self.num_batches):
            winner = self._train_game(player1, player2)
            stats[winner] += 1

        self._show_stats(stat_type, stats)
        return stats

    def _init_stats(self):
        return {Board.X: 0, Board.O: 0, Board.DRAW: 0}
        
    def _train_game(self, player1, player2):
        controller = GameController(player1, player2)
        winner = None
        while winner is None:
            winner, _ = controller.make_move()
            run_if_learner(player1, lambda: player1.store_state())
            run_if_learner(player2, lambda: player2.store_state())
            
        run_if_learner(player1, lambda: player1.set_reward(winner))
        run_if_learner(player2, lambda: player2.set_reward(winner))
        return winner

    def _save_stats(self, stats):
        with open(utils.get_path("data", self.player1.__class__.__name__ + "Stats.pkl"), "wb") as f:
            params = {"num_games": self.num_games, "num_batches": self.num_batches}
            pickle.dump({"params": params, "stats": stats}, f)

    def _show_stats(self, stat_type, stats):
        print("- {}: X wins={}, O wins={}, Draw={}".format(
            stat_type, stats[Board.X], stats[Board.O], stats[Board.DRAW]))
        return stats

    def _compete_batch(self, player1, player2, stat_type):
        run_if_learner(player1, lambda: player1.disable_learning())
        run_if_learner(player2, lambda: player2.disable_learning())

        stats = self._init_stats()
        for batch_number in range(self.num_batches):
            winner = self._compete_game(player1, player2)
            stats[winner] += 1

        self._show_stats(stat_type, stats)
        return stats
        
    def _compete_game(self, player1, player2):
        controller = GameController(player1, player2)
        winner = None
        while winner is None:
            winner, _ = controller.make_move()
        return winner

    def save(self, stats):
        self.player1.save()
        self.player2.save()
        self._save_stats(stats)

    def show_num_states(self):
        print("X has trained {} states".format(self.player1.get_num_states()))
        print("O has trained {} states".format(self.player2.get_num_states()))

def main(args=sys.argv[1:]):
    trainer = Trainer(args)
    stats = trainer.train()
    trainer.save(stats)
    trainer.show_num_states()
    return 0

if __name__ == "__main__":
    sys.exit(main())
