import sys
import argparse
import textwrap
import pickle
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import utils
import player_types
from board import Board
from game_controller import GameController

class Visualizer(object):
    def __init__(self, args):
        parsed_args = self._parse_args(args)
        self.player1 = self._init_player(parsed_args, Board.X)
        self.player2 = self._init_player(parsed_args, Board.O)

    def _parse_args(self, args):
        epilog = "\n".join(
            "- {}: {}".format(type, description)
            for type, description in zip(player_types.get_learning_player_types(), 
                                         player_types.get_learning_player_descriptions()))
        parser = argparse.ArgumentParser(
            description="Visualize Machine Learning Tic-Tac-Toe Training",
            formatter_class=argparse.RawTextHelpFormatter,
            epilog=textwrap.dedent("where LEARNING_TYPE is as follows:\n" +
                                   player_types.get_learning_player_command_line_args()))
        parser.add_argument(
            "-l", "--learning-type", choices=player_types.get_learning_player_types(),
            default="TD", dest="learning_type", metavar="LEARNING_TYPE")
        return parser.parse_args(args)

    def _init_player(self, parsed_args, piece):
        player = player_types.get_learning_player(parsed_args.learning_type)
        player.load(piece)
        return player

    def visualize(self):
        stats = self._load_stats()
        self._plot_stats(stats)
        self._plot_best_moves()

    def _load_stats(self):
        with open(utils.get_path("data", self.player1.__class__.__name__ + "Stats.pkl"), "rb") as f:
            stat_info = pickle.load(f)
            self.num_games = stat_info["params"]["num_games"]
            self.num_batches = stat_info["params"]["num_batches"]
            return stat_info["stats"]

    def _plot_stats(self, stats):
        self._plot_stats_figure("Training", stats, "train")
        self._plot_stats_figure("Competing", stats, "compete")
        
    def _plot_stats_figure(self, title, stats, key_prefix):
        f, ax = plt.subplots(3, 1, sharex=True)
        plt.suptitle("{} - {} game trials".format(title, self.num_batches))
        lines = self._plot_stats_subplot(
            ax[0], "Self", stats[key_prefix+ "_self"], [Board.O, Board.X])
        self._plot_stats_subplot(
            ax[1], "X vs Random", stats[key_prefix + "_x_vs_random"], [Board.O])
        self._plot_stats_subplot(
            ax[2], "O vs Random", stats[key_prefix + "_o_vs_random"], [Board.X])
        plt.xlabel("Game #")
        f.subplots_adjust(hspace=0.1)
        f.legend(lines, ["X Losses", "O Losses"], "upper right")
        plt.show()
    
    def _plot_stats_subplot(self, ax, ylabel, stats, keys):
        x = list(range(self.num_batches, self.num_games + self.num_batches, self.num_batches))
        colors = {Board.O: "r", Board.X: "b"}
        markers = {Board.O: "x", Board.X: "o"}
        lines = []
        for key in keys:
            y = [stat[key] for stat in stats]
            lines += ax.plot(x, y, c=colors[key], marker=markers[key], markersize=5)
            
        ax.set_ylabel(ylabel)
        ax.grid()
        return lines

    def _plot_best_moves(self):
        game_controller = GameController(self.player1, self.player2)
        f, ax = plt.subplots(3, 3)
        f.suptitle("Best moves")
        f.subplots_adjust(hspace=0.25, wspace=-0.25, bottom=0.0)
        winner = None
        move_number = 0
        while winner is None:
            row = move_number // 3
            col = move_number % 3
            self._plot_best_move(ax[row][col], game_controller)
            winner, _ = game_controller.make_move()
            move_number += 1
        plt.show()

    def _plot_best_move(self, ax, game_controller):
        self._plot_move_values(ax, game_controller)
        self._plot_pieces(ax, game_controller)

    def _plot_move_values(self, ax, game_controller):
        cmaps = {Board.X: "RdBu_r", Board.O: "RdBu"}
        player = game_controller.get_player()
        move_values = player.get_move_values()
        positions = range(len(game_controller.board.state))
        values = [move_values.get(position, 0.0) for position in positions]
        masks = [position not in move_values for position in positions]
        sns.heatmap(np.array(values).reshape((3, 3)), annot=True, linewidths=1.0, linecolor="k",
                    square=True, vmin=0.0, vmax=1.0, xticklabels=False, yticklabels=False, cbar=False,
                    cmap=cmaps[player.piece], mask=np.array(masks).reshape((3, 3)), ax=ax)
        ax.set_title(Board.format_piece(player.piece) + "'s Turn")

    def _plot_pieces(self, ax, game_controller):
        colors = {Board.X: "red", Board.O: "blue"}
        for position, piece in enumerate(game_controller.board.state):
            x = position % 3
            y = position // 3
            if piece != Board.EMPTY:
                 font = {"color": colors[piece], "size": 16}
                 ax.text(x+0.5, y+0.5, Board.format_piece(piece), fontdict=font, ha="center", va="center")

def main(args=sys.argv[1:]):
    is_windows = sys.platform.lower().startswith("win")
    if is_windows:
        print("Close the current graph to see the next one")
    else:
        plt.interactive(True)

    visualizer = Visualizer(args)
    visualizer.visualize()

    if not is_windows:
        input("Press ENTER to continue...")
    return 0

if __name__ == "__main__":
    sys.exit(main())

