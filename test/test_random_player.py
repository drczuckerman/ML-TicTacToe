import unittest
from mock import patch, Mock
from random_player import RandomPlayer
from computer_player import run_if_computer
from learning_computer_player import run_if_learner
from human_player import run_if_human
from board import Board
from board_test_utils import assert_get_move_is, assert_get_move_values_are
from mock_random import MockRandom

class TestRandomPlayer(unittest.TestCase):
    def setUp(self):
        self.player = RandomPlayer()
        self.board = Board()
        self.player.set_board(self.board)
        self.func = Mock()

    def test_constructor_initializes_board_and_piece_to_none(self):
        player = RandomPlayer()
        self.assertIsNone(player.piece)
        self.assertIsNone(player.board)

    def test_set_board(self):
        self.assertEqual(self.board, self.player.board)

    def test_set_piece(self):
        player1 = RandomPlayer()
        player1.set_piece(Board.X)
        self.assertEqual(Board.X, player1.piece)

        player2 = RandomPlayer()
        player2.set_piece(Board.O)
        self.assertEqual(Board.O, player2.piece)

    @patch('random_player.random.choice')
    def test_get_move_returns_random_available_move(self, choice_mock):
        choice_mock.side_effect = MockRandom(5).choice
        assert_get_move_is(self, self.player, self.board, 7, Board.X, "---|-XO|---")

    def test_indicate_move(self):
        self.assertEqual("My move is 4", self.player.indicate_move(3))

    def test_run_if_computer_runs_function_if_random_player(self):
        run_if_computer(self.player, self.func)
        self.func.assert_called_once_with()

    def test_run_if_learner_does_not_run_function_if_random_player(self):
        run_if_learner(self.player, self.func)
        self.func.assert_not_called()

    def test_run_if_human_does_not_run_function_if_random_player(self):
        run_if_human(self.player, self.func)
        self.func.assert_not_called()
