import unittest
import player_types
from mock import patch, call
from io import StringIO
from board import Board
from human_player import HumanPlayer
from random_player import RandomPlayer
from td_learning_player import TDLearningPlayer
from td_symmetric_learning_player import TDSymmetricLearningPlayer
from learning_computer_player import LearningComputerPlayer
from console_game import ConsoleGame, main
from board_test_utils import get_expected_formatted_board

class MockLearningPlayer(LearningComputerPlayer):
    def __init__(self, piece):
        self.set_piece(piece)

    def load(self, piece):
        self.set_piece(piece)

class ConsoleGameSpy(ConsoleGame):
    def __init__(self, actions):
        self.calls = []
        self.actions = actions
        self.action_indices = {"select_players": 0, "get_action": 0}

    def _select_players(self):
         self._report_call("select_players")
         action = self._get_next_action("select_players")
         return action["x_player"](), action["o_player"]()

    def play_one_game(self, player1, player2):
        self._report_call("play_one_game", player1.__class__, player2.__class__)

    def _get_action(self):
        self._report_call("get_action")
        return self._get_next_action("get_action")

    def _swap_players(self, player1, player2):
        self._report_call("swap_players")
        return player2, player1

    def _report_call(self, action_type, *args):
        self.calls.append((action_type,) + args)

    def _get_next_action(self, action_type):
        index = self.action_indices[action_type]
        action = self.actions[action_type][index]
        self.action_indices[action_type] = index + 1
        return action

class TestConsoleGame(unittest.TestCase):
    def setUp(self):
        self.human1 = HumanPlayer()
        self.human2 = HumanPlayer()
        self.random1 = RandomPlayer()
        self.random2 = RandomPlayer()
        self.console = ConsoleGame()

    @patch('sys.stdout', new_callable=StringIO)
    @patch('builtins.input')
    def assert_play_one_human_game_outputs(
            self, input_mock, stdout_mock, moves, formatted_pieces_list, result):
        input_mock.side_effect = moves

        expected_output = ""
        expected_piece = "X"
        for formatted_pieces in formatted_pieces_list[:-1]:
            if formatted_pieces == "m":
                expected_output = expected_output[:-1] + "Invalid move\n\n" # delete last newline
                continue

            expected_output += self.get_turn_output(expected_piece, formatted_pieces)
            expected_output += "\n"
            expected_piece = self.invert_expected_piece(expected_piece)

        expected_output += self.get_game_over_output(result, formatted_pieces_list[-1])

        self.assertEqual(result, self.console.play_one_game(self.human1, self.human2))
        self.assertEqual(expected_output, stdout_mock.getvalue())

    def get_turn_output(self, expected_piece, formatted_pieces):
        expected_output = "It's your turn, " + expected_piece + "\n"
        expected_output += get_expected_formatted_board(formatted_pieces)
        return expected_output

    def invert_expected_piece(self, expected_piece):
        return "O" if expected_piece == "X" else "X"

    def get_game_over_output(self, result, formatted_pieces):
        expected_output = "Game over\n"
        expected_output += get_expected_formatted_board(formatted_pieces)

        if result == Board.X:
            expected_output += "X Wins"
        elif result == Board.O:
            expected_output += "O Wins"
        else:
            expected_output += "Draw"
        expected_output += "\n"
        
        expected_output += "\n"
        return expected_output

    @patch('sys.stdout', new_callable=StringIO)
    @patch('random.choice')
    def assert_play_one_random_game_outputs(
            self, random_mock, stdout_mock, moves, formatted_pieces_list, result):
        random_mock.side_effect = moves

        expected_output = ""
        expected_piece = "X"
        for formatted_pieces, move in zip(formatted_pieces_list[:-1], moves):
            expected_output += self.get_turn_output(expected_piece, formatted_pieces)
            expected_output += "My move is {}\n".format(move + 1)
            expected_output += "\n"
            expected_piece = self.invert_expected_piece(expected_piece)

        expected_output += self.get_game_over_output(result, formatted_pieces_list[-1])

        self.assertEqual(result, self.console.play_one_game(self.random1, self.random2))
        self.assertEqual(expected_output, stdout_mock.getvalue())

    @patch('sys.stdout', new_callable=StringIO)
    @patch('builtins.input')
    def assert_select_player_selects(self, input_mock, stdout_mock, piece, menu_items, player_class):
        input_mock.side_effect = menu_items
        player = self.console._select_player(piece)
        self.assertIsInstance(player, player_class)

        expected_output = "Select {} player:\n".format(Board.format_piece(piece))
        for item_num, description in enumerate(player_types.get_player_descriptions(), start=1):
            expected_output += "{}) {}\n".format(item_num, description)

        expected_output += "Invalid selection\n"*(len(menu_items) - 1)
        expected_output += "\n"
        self.assertEqual(expected_output, stdout_mock.getvalue())
        self.assertEqual([call("Select player: ")]*len(menu_items), input_mock.call_args_list)

    @patch('sys.stdout', new_callable=StringIO)
    @patch('builtins.input')
    def assert_action_is(self, input_mock, stdout_mock, menu_items, action):
        input_mock.side_effect = menu_items
        self.assertEqual(action, self.console._get_action())
        
        expected_output = """\
Select action:
1) Same players and pieces
2) Same players and different pieces
3) Different players
4) Quit
"""
        expected_output += "Invalid selection\n"*(len(menu_items) - 1)
        expected_output += "\n"
        self.assertEqual(expected_output, stdout_mock.getvalue())
        self.assertEqual([call("Select action: ")]*len(menu_items), input_mock.call_args_list)

    def assert_swap_players_are(self, x_player, o_player):
        new_x_player, new_o_player = self.console.swap_players(x_player, o_player)
        self.assertEqual(new_x_player, o_player)
        self.assertEqual(new_o_player, x_player)

    def assert_play_does(self, actions, expected_calls):
        console_spy = ConsoleGameSpy(actions)
        console_spy.play()
        self.assertEqual(expected_calls, console_spy.calls)

    def test_play_one_human_game_stops_when_x_wins(self):
        self.assert_play_one_human_game_outputs(
            moves=["1", "4", "2", "5", "3"],
            formatted_pieces_list=["---|---|---",
                                   "x--|---|---",
                                   "x--|o--|---",
                                   "xx-|o--|---",
                                   "xx-|oo-|---",
                                   "XXX|oo-|---"],
            result=Board.X)

    def test_play_one_human_game_stops_when_o_wins(self):
        self.assert_play_one_human_game_outputs(
            moves=["7", "5", "9", "8", "4", "2"],
            formatted_pieces_list=["---|---|---",
                                   "---|---|x--",
                                   "---|-o-|x--",
                                   "---|-o-|x-x",
                                   "---|-o-|xox",
                                   "---|xo-|xox",
                                   "-O-|xO-|xOx"],
            result=Board.O)

    def test_play_one_human_game_stops_when_draw(self):
        self.assert_play_one_human_game_outputs(
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

    def test_play_one_human_game_indicates_when_move_is_invalid(self):
        self.assert_play_one_human_game_outputs(
            moves=["5", "5", "3", "9", "6", "1"],
            formatted_pieces_list=["---|---|---",
                                   "---|-x-|---",
                                   "m",
                                   "--o|-x-|---",
                                   "--o|-x-|--x",
                                   "--o|-xo|--x",
                                   "X-o|-Xo|--X"],
            result=Board.X)

    def test_play_one_random_game_stops_when_x_wins(self):
        self.assert_play_one_random_game_outputs(
            moves=[3, 5, 0, 8, 6],
            formatted_pieces_list=["---|---|---",
                                   "---|x--|---",
                                   "---|x-o|---",
                                   "x--|x-o|---",
                                   "x--|x-o|--o",
                                   "X--|X-o|X-o"],
            result=Board.X)

    def test_play_one_random_game_stops_when_o_wins(self):
        self.assert_play_one_random_game_outputs(
            moves=[4, 8, 1, 7, 2, 6],
            formatted_pieces_list=["---|---|---",
                                   "---|-x-|---",
                                   "---|-x-|--o",
                                   "-x-|-x-|--o",
                                   "-x-|-x-|-oo",
                                   "-xx|-x-|-oo",
                                   "-xx|-x-|OOO"],
            result=Board.O)

    def test_play_one_random_game_stops_when_draw(self):
        self.assert_play_one_random_game_outputs(
            moves=[6, 7, 8, 4, 3, 5, 1, 0, 2],
            formatted_pieces_list=["---|---|---",
                                   "---|---|x--",
                                   "---|---|xo-",
                                   "---|---|xox",
                                   "---|-o-|xox",
                                   "---|xo-|xox",
                                   "---|xoo|xox",
                                   "-x-|xoo|xox",
                                   "ox-|xoo|xox",
                                   "oxx|xoo|xox"],
            result=Board.DRAW)

    def test_select_player_for_x_human(self):
        self.assert_select_player_selects(
            piece=Board.X,
            menu_items=[" 1 "],
            player_class=HumanPlayer)

    def test_select_player_for_o_random(self):
        self.assert_select_player_selects(
            piece=Board.O,
            menu_items=["2"],
            player_class=RandomPlayer)

    @patch('td_learning_player.TDLearningPlayer.load')
    def test_select_player_for_x_td_learning_player_loads_values(self, load_mock):
        self.assert_select_player_selects(
            piece=Board.X,
            menu_items=["3"],
            player_class=TDLearningPlayer)
        load_mock.assert_called_once_with(Board.X)

    @patch('td_symmetric_learning_player.TDSymmetricLearningPlayer.load')
    def test_select_player_for_x_td_symmetric_learning_player_loads_values(self, load_mock):
        self.assert_select_player_selects(
            piece=Board.X,
            menu_items=["4"],
            player_class=TDLearningPlayer)
        load_mock.assert_called_once_with(Board.X)

    def test_select_player_indicates_invalid_selection(self):
        self.assert_select_player_selects(
            piece=Board.X,
            menu_items=["0", str(len(player_types.get_player_types()) + 1), "X", "1"],
            player_class=HumanPlayer)

    @patch('console_game.ConsoleGame._select_player')
    def test_select_players(self, select_mock):
        select_mock.side_effect = [RandomPlayer(), HumanPlayer()]
        player1, player2 = self.console._select_players()
        self.assertIsInstance(player1, RandomPlayer)
        self.assertIsInstance(player2, HumanPlayer)
        self.assertEqual([call(Board.X), call(Board.O)], select_mock.call_args_list)

    def test_get_action_quit(self):
        self.assert_action_is(
            menu_items=[" 4 "],
            action=ConsoleGame.ACTION_QUIT)

    def test_get_action_same_players_and_pieces(self):
        self.assert_action_is(
            menu_items=["1"],
            action=ConsoleGame.ACTION_SAME_PLAYERS_AND_PIECES)

    def test_get_action_same_players_diff_pieces(self):
        self.assert_action_is(
            menu_items=["2"],
            action=ConsoleGame.ACTION_SAME_PLAYERS_DIFF_PIECES)

    def test_get_action_diff_players(self):
        self.assert_action_is(
            menu_items=["3"],
            action=ConsoleGame.ACTION_DIFF_PLAYERS)

    def test_get_action_invalid_actions(self):
        self.assert_action_is(
            menu_items=["0", "5", "X", "4"],
            action=ConsoleGame.ACTION_QUIT)

    def test_swap_players_swaps_non_learners(self):
        self.assert_swap_players_are(
            x_player=HumanPlayer(),
            o_player=RandomPlayer())

    def test_swap_players_swaps_and_reloads_learners(self):
        player1 = MockLearningPlayer(Board.X)
        player2 = MockLearningPlayer(Board.O)
        self.assert_swap_players_are(
            x_player=player1,
            o_player=player2)
        self.assertEqual(Board.O, player1.piece)
        self.assertEqual(Board.X, player2.piece)

    def test_play_and_quit(self):
        self.assert_play_does(
            actions=\
            {
                "select_players": [{"x_player": HumanPlayer, "o_player": RandomPlayer}],
                "get_action": [ConsoleGame.ACTION_QUIT]
            },
            expected_calls=\
            [
                ("select_players",),
                ("play_one_game", HumanPlayer, RandomPlayer),
                ("get_action",)
            ]
        )

    def test_play_and_same_players_and_pieces(self):
        self.assert_play_does(
            actions=\
            {
                "select_players": [{"x_player": RandomPlayer, "o_player": TDLearningPlayer}],
                "get_action": [ConsoleGame.ACTION_SAME_PLAYERS_AND_PIECES, ConsoleGame.ACTION_QUIT]
            },
            expected_calls=\
            [
                ("select_players",),
                ("play_one_game", RandomPlayer, TDLearningPlayer),
                ("get_action",),
                ("play_one_game", RandomPlayer, TDLearningPlayer),
                ("get_action",)
            ]
        )

    def test_play_and_same_players_and_diff_pieces(self):
        self.assert_play_does(
            actions=\
            {
                "select_players": [{"x_player": HumanPlayer, "o_player": TDLearningPlayer}],
                "get_action": [ConsoleGame.ACTION_SAME_PLAYERS_DIFF_PIECES, ConsoleGame.ACTION_QUIT]
            },
            expected_calls=\
            [
                ("select_players",),
                ("play_one_game", HumanPlayer, TDLearningPlayer),
                ("get_action",),
                ("swap_players",),
                ("play_one_game", TDLearningPlayer, HumanPlayer),
                ("get_action",)
            ]
        )

    def test_play_and_diff_players(self):
        self.assert_play_does(
            actions=\
            {
                "select_players": \
                [
                    {"x_player": RandomPlayer, "o_player": TDLearningPlayer},
                    {"x_player": HumanPlayer, "o_player": RandomPlayer}
                ],
                "get_action": [ConsoleGame.ACTION_DIFF_PLAYERS, ConsoleGame.ACTION_QUIT]
            },
            expected_calls=\
            [
                ("select_players",),
                ("play_one_game", RandomPlayer, TDLearningPlayer),
                ("get_action",),
                ("select_players",),
                ("play_one_game", HumanPlayer, RandomPlayer),
                ("get_action",)
            ]
        )

    @patch('console_game.ConsoleGame.play')
    def test_main(self, play_mock):
        self.assertEqual(0, main([]))
        play_mock.assert_called_once_with()
