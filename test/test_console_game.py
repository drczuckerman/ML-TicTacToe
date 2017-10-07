import unittest
from mock import patch
from io import StringIO
from board import Board
from human_player import HumanPlayer
from console_game import ConsoleGame
from board_test_utils import get_expected_formatted_board

class TestConsoleGame(unittest.TestCase):
    def setUp(self):
        self.human1 = HumanPlayer()
        self.human2 = HumanPlayer()
        self.console = ConsoleGame()

    @patch('sys.stdout', new_callable=StringIO)
    @patch('builtins.input')
    def assert_play_one_game_outputs(self, input_mock, stdout_mock, moves, formatted_pieces_list, result):
        input_mock.side_effect = moves

        expected_output = ""
        expected_piece = "X"
        for formatted_pieces in formatted_pieces_list[:-1]:
            if formatted_pieces == "m":
                expected_output = expected_output[:-1] + "Invalid move\n\n" # delete last newline
                continue

            expected_output += "It's your turn, " + expected_piece + "\n"
            expected_output += get_expected_formatted_board(formatted_pieces)
            expected_output += "\n"
            expected_piece = "O" if expected_piece == "X" else "X"

        expected_output += "Game over\n"
        expected_output += get_expected_formatted_board(formatted_pieces_list[-1])

        if result == Board.X:
            expected_output += "X Wins"
        elif result == Board.O:
            expected_output += "O Wins"
        else:
            expected_output += "Draw"
        expected_output += "\n"

        self.assertEqual(result, self.console.play_one_game(self.human1, self.human2))
        self.assertEqual(expected_output, stdout_mock.getvalue())

    def test_play_one_game_stops_when_x_wins(self):
        self.assert_play_one_game_outputs(
            moves=["1", "4", "2", "5", "3"],
            formatted_pieces_list=["---|---|---",
                                   "x--|---|---",
                                   "x--|o--|---",
                                   "xx-|o--|---",
                                   "xx-|oo-|---",
                                   "XXX|oo-|---"],
            result=Board.X)

    def test_play_one_game_stops_when_o_wins(self):
        self.assert_play_one_game_outputs(
            moves=["7", "5", "9", "8", "4", "2"],
            formatted_pieces_list=["---|---|---",
                                   "---|---|x--",
                                   "---|-o-|x--",
                                   "---|-o-|x-x",
                                   "---|-o-|xox",
                                   "---|xo-|xox",
                                   "-O-|xO-|xOx"],
            result=Board.O)

    def test_play_one_game_stops_when_draw(self):
        self.assert_play_one_game_outputs(
            moves=["3", "5", "9", "6", "4", "2", "8", "7", "1"],
            formatted_pieces_list=["---|---|---",
                                   "--x|---|---",
                                   "--x|-o-|---",
                                   "--x|-o-|--x",
                                   "--x|-oo|--x",
                                   "--x|xoo|--x",
                                   "-ox|xoo|--x",
                                   "-ox|xoo|-xx",
                                   "-ox|xoo|oxx",
                                   "xox|xoo|oxx"],
            result=Board.DRAW)

    def test_play_one_game_indicates_when_move_is_invalid(self):
        self.assert_play_one_game_outputs(
            moves=["5", "5", "3", "9", "6", "1"],
            formatted_pieces_list=["---|---|---",
                                   "---|-x-|---",
                                   "m",
                                   "--o|-x-|---",
                                   "--o|-x-|--x",
                                   "--o|-xo|--x",
                                   "X-o|-Xo|--X"],
            result=Board.X)
