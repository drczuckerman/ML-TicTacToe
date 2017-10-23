import unittest
from mock import patch
from board_test_utils import set_board, get_board_state_tuple
from web_game import WebGame
from board import Board
from game_controller import GameController
from human_player import HumanPlayer
from random_player import RandomPlayer
from td_learning_player import TDLearningPlayer

class TestWebGame(unittest.TestCase):
    def setUp(self):
        self.game = WebGame()

    def set_loaded(self, piece):
        self.loaded[piece] = True

    @patch('learning_computer_player.LearningComputerPlayer._load_file')
    def assert_start_game_does(
            self, load_mock, player_types_dict, player1_class, player2_class,
            expected_player1_loaded=False, expected_player2_loaded=False):
        load_mock.side_effect = lambda piece: self.set_loaded(piece)
        self.loaded = {Board.X: False, Board.O: False}

        self.assert_game_info_is(None, [], Board.X, "---|---|---", self.game.start_game(player_types_dict))

        self.assertIsInstance(self.game.player1, player1_class)
        self.assertIsInstance(self.game.player2, player2_class)
        self.assert_is_non_interactive_if_human(player_types_dict["x"], self.game.player1)
        self.assert_is_non_interactive_if_human(player_types_dict["o"], self.game.player2)
        self.assertEqual(expected_player1_loaded, self.loaded[Board.X])
        self.assertEqual(expected_player2_loaded, self.loaded[Board.O])
        self.assertIsInstance(self.game.controller, GameController)
        self.assertEqual(
            {Board.X: player_types_dict["x"], Board.O: player_types_dict["o"]},
            self.game.player_types_dict)

    def assert_is_non_interactive_if_human(self, player_type, player):
        if player_type == "Human":
            self.assertFalse(player.interactive)

    def assert_game_info_is(self, winner, winning_positions, turn, pieces, game_info):
        expected_game_info = \
        {
            "winner": winner,
            "winning_positions": winning_positions,
            "turn": turn,
            "board": list(get_board_state_tuple(pieces))
        }
        self.assertEqual(expected_game_info, game_info)

    def test_constructor_initializes_controller(self):
        self.assertIsNone(self.game.controller)

    def test_constructor_initializes_players(self):
        self.assertIsNone(self.game.player1)
        self.assertIsNone(self.game.player2)

    def test_constructor_initialize_player_types_dict(self):
        self.assertEqual({Board.X: "", Board.O: ""}, self.game.player_types_dict)

    def test_start_game_sets_non_interactive_humans(self):
        self.assert_start_game_does(
            player_types_dict={"x": "Human", "o": "Human"},
            player1_class=HumanPlayer,
            player2_class=HumanPlayer)

    def test_start_game_loads_learning_players(self):
        self.assert_start_game_does(
            player_types_dict={"x": "TD", "o": "TD"},
            player1_class=TDLearningPlayer,
            player2_class=TDLearningPlayer,
            expected_player1_loaded=True,
            expected_player2_loaded=True)

    def test_start_game_loads_learning_players_once_if_same_player_type(self):
        self.assert_start_game_does(
            player_types_dict={"x": "TD", "o": "Random"},
            player1_class=TDLearningPlayer,
            player2_class=RandomPlayer,
            expected_player1_loaded=True,
            expected_player2_loaded=False)
        self.assert_start_game_does(
            player_types_dict={"x": "TD", "o": "Random"},
            player1_class=TDLearningPlayer,
            player2_class=RandomPlayer,
            expected_player1_loaded=False,
            expected_player2_loaded=False)

    def test_start_game_loads_learning_players_when_diff_player_type(self):
        self.assert_start_game_does(
            player_types_dict={"x": "TD", "o": "Random"},
            player1_class=TDLearningPlayer,
            player2_class=RandomPlayer,
            expected_player1_loaded=True,
            expected_player2_loaded=False)
        self.assert_start_game_does(
            player_types_dict={"x": "Random", "o": "TD"},
            player1_class=RandomPlayer,
            player2_class=TDLearningPlayer,
            expected_player1_loaded=False,
            expected_player2_loaded=True)

    @patch('random_player.RandomPlayer.get_move')
    def test_make_computer_move(self, get_move_mock):
        get_move_mock.return_value = 4
        self.game.start_game({"x": "Random", "o": "Human"})
        set_board(self.game.controller.board, "XXO|O-X|OOX")
        self.assert_game_info_is(Board.X, [0, 4, 8], Board.O, "XXO|OXX|OOX", self.game.make_computer_move())

    @patch('random_player.RandomPlayer.get_move')
    def test_make_human_move(self, get_move_mock):
        get_move_mock.return_value = 6
        self.game.start_game({"x": "Random", "o": "Human"})
        self.game.make_computer_move()
        set_board(self.game.controller.board, "OXX|O-X|---")
        self.assert_game_info_is(
            Board.O, [0, 3, 6], Board.X, "OXX|O-X|O--", self.game.make_human_move(" 7 "))
