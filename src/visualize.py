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
        parser = argparse.ArgumentParser(
            description="Visualize Machine Learning Tic-Tac-Toe Training",
            formatter_class=argparse.RawTextHelpFormatter,
            epilog=textwrap.dedent("where LEARNING_TYPE is as follows:\n" +
                                   "\n".join(player_types.get_learning_player_descriptions())))
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
        self._plot_ideal_moves()

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
        colors = {Board.O: "r", Board.X: "g"}
        markers = {Board.O: "x", Board.X: "o"}
        lines = []
        for key in keys:
            y = [stat[key] for stat in stats]
            lines += ax.plot(x, y, c=colors[key], marker=markers[key], markersize=5)
            
        ax.set_ylabel(ylabel)
        ax.grid()
        return lines

    def _plot_ideal_moves(self):
        game_controller = GameController(self.player1, self.player2)
        color_dict = {"X": "red", "O": "green"}
        f, ax = plt.subplots(3, 3)
        f.suptitle("Best moves")
        f.subplots_adjust(hspace=0.25, wspace=-0.25, bottom=0.0)
        for move in range(9):
            row = move // 3
            col = move % 3
            values = []
            mask = [False]*9
            pieces = [" "]*9
            player = game_controller.get_player()
            for k in range(9):
                piece = game_controller.board.state[k]
                if piece != Board.EMPTY:
                    values.append(0)
                    mask[k] = True
                    pieces[k] = Board.format_piece(piece)
                    continue
                with game_controller.board.try_move(k, player.piece) as (winner, state):
                    values.append(player._get_value(state, winner))

            sns.heatmap(np.array(values).reshape((3, 3)), annot=True, linewidths=1.0, linecolor="k",
                        square=True, vmin=0.0, vmax=1.0, xticklabels=False, yticklabels=False, cbar=False,
                        cmap="RdBu_r", mask=np.array(mask).reshape((3, 3)), ax=ax[row][col])
            ax[row][col].set_title(Board.format_piece(player.piece) + "'s Turn")

            for k, piece in enumerate(pieces):
                x = k % 3
                y = k // 3
                if piece != " ":
                     font = {"color": color_dict[piece], "size": 16}
                     ax[row][col].text(x+0.5, y+0.5, pieces[k], fontdict=font, 
                                       ha="center", va="center")

            game_controller.make_move()

def main(args=sys.argv[1:]):
    plt.interactive(True)
    visualizer = Visualizer(args)
    visualizer.visualize()
    input("Press ENTER to continue...")
    return 0

if __name__ == "__main__":
    sys.exit(main())

