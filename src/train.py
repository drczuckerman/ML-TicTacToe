import sys
import argparse
import textwrap
from matplotlib import pyplot as plt
from td_learning_player import TDLearningPlayer
from random_player import RandomPlayer
from board import Board
from game_controller import GameController

class Trainer(object):
    LEARNERS = {"TD": TDLearningPlayer}
    
    def __init__(self, args):
        parsed_args = self._parse_args(args)
        self.num_games = parsed_args.num_games
        self.num_batches = parsed_args.num_batches
        self.player1 = self._init_class(parsed_args)
        self.player2 = self._init_class(parsed_args)
        self.random_player = RandomPlayer()
        
    def _parse_args(self, args):
        parser = argparse.ArgumentParser(
            description="Train ML Tic-Tac-Toe Players",
            formatter_class=argparse.RawTextHelpFormatter)
        parser.add_argument(
            "-g", "--num-games", default=20000, type=int, help="number of games to play")
        parser.add_argument(
            "-b", "--num-batches", default=1000, type=int, help="number of batches to gather stats")
        parser.add_argument(
            "-l", "--learning-type", choices=["TD"], default="TD", dest="learning_type", metavar="LEARNING_TYPE",
            help=textwrap.dedent("""\
where LEARNING_TYPE is as follows:
- TD=Temporal Difference Learning"""))
        parser.add_argument("-a", "--alpha", type=float, help="learning rate")
        parser.add_argument("-e", "--epsilon", type=float, help="exploration rate")
        parser.add_argument("-x", "--x-draw-reward", type=float, help="X draw reward")
        parser.add_argument("-o", "--o-draw", type=float, help="O draw reward")
        return parser.parse_args(args)

    def _init_class(self, parsed_args):
        player = self.LEARNERS[parsed_args.learning_type]()
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
        stats = self._init_stats()
        for batch_number in range(self.num_batches):
            winner = self._train_game(player1, player2)
            stats[winner] += 1

        self._show_stats(stat_type, stats)
        return stats

    def _init_stats(self):
        return {Board.X: 0, Board.O: 0, Board.DRAW: 0}
        
    def _show_stats(self, stat_type, stats):
        print("- {}: X wins={}, O wins={}, Draw={}".format(
            stat_type, stats[Board.X], stats[Board.O], stats[Board.DRAW]))
        return stats

    def _train_game(self, player1, player2):
        controller = GameController(player1, player2)
        winner = None
        while winner is None:
            winner = controller.make_move()
            player1.store_state()
            player2.store_state()
            
        player1.set_reward(winner)
        player2.set_reward(winner)
        return winner

    def _compete_batch(self, player1, player2, stat_type):
        player1.disable_learning()
        player2.disable_learning()

        stats = self._init_stats()
        for batch_number in range(self.num_batches):
            winner = self._compete_game(player1, player2)
            stats[winner] += 1

        self.player1.enable_learning()
        self.player2.enable_learning()

        self._show_stats(stat_type, stats)
        return stats
        
    def _compete_game(self, player1, player2):
        controller = GameController(player1, player2)
        winner = None
        while winner is None:
            winner = controller.make_move()
        return winner

    def plot_stats(self, stats):
        self._plot_figure("Training", stats, "train")
        self._plot_figure("Competing", stats, "compete")
        
    def _plot_figure(self, title, stats, key_prefix):
        f, ax = plt.subplots(3, 1)
        ax[0].set_title("{} - {} game trials".format(title, self.num_batches))
        self._plot_stats_subplot(
            ax[0], "Self", stats[key_prefix+ "_self"], [Board.O, Board.X], True)
        self._plot_stats_subplot(
            ax[1], "X vs Random", stats[key_prefix + "_x_vs_random"], [Board.O], False)
        self._plot_stats_subplot(
            ax[2], "O vs Random", stats[key_prefix + "_o_vs_random"], [Board.X], False)
        plt.xlabel("Game #")
        f.subplots_adjust(hspace=0.35)
        plt.show()
    
    def _plot_stats_subplot(self, ax, ylabel, stats, keys, show_legend):
        x = list(range(self.num_batches, self.num_games + self.num_batches, self.num_batches))
        colors = {Board.O: "r", Board.X: "g"}
        markers = {Board.O: "x", Board.X: "o"}
        for key in keys:
            y = [stat[key] for stat in stats]
            ax.plot(x, y, c=colors[key], marker=markers[key], markersize=5)
            
        ax.set_ylabel(ylabel)
        ax.grid()

        box = ax.get_position()
        ax.set_position([box.x0, box.y0, box.width*0.9, box.height])
        if show_legend:
            ax.legend(["X Losses", "O Losses"], loc="center left", bbox_to_anchor=(1,0.5))
            
    def show_num_states(self):
        print("X has trained {} states".format(len(self.player1.values)))
        print("O has trained {} states".format(len(self.player2.values)))

def main(args=sys.argv[1:]):
    plt.interactive(True)
    trainer = Trainer(args)
    stats = trainer.train()
    trainer.plot_stats(stats)
    trainer.show_num_states()
    input("Press ENTER to continue...")
    return 0

if __name__ == "__main__":
    sys.exit(main())
