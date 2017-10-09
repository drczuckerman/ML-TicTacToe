import unittest
from mock import patch
from random_player import RandomPlayer
from board import Board
from board_test_utils import assert_get_move_is
from mock_random import MockRandom

class TestRandomPlayer(unittest.TestCase):
    def setUp(self):
        self.player = RandomPlayer()
        self.board = Board()
        self.player.set_board(self.board)

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

    def test_reset(self):
        self.player.reset()
        # Should not assert
        
    def test_set_params(self):
        self.player.set_params(foo=1, bar=2)
        # Should not assert

    def test_store_state(self):
        self.player.store_state()
        # Should not assert

    def test_set_reward(self):
        self.player.set_reward(Board.X)
        # Should not assert

    def test_disable_learning(self):
        self.player.disable_learning()
        # Should not assert

    def test_enable_learning(self):
        self.player.enable_learning()
        # Should not assert

    @patch('random_player.random.choice')
    def test_get_move_returns_random_available_move(self, choice_mock):
        choice_mock.side_effect = MockRandom(5).choice
        assert_get_move_is(self, self.player, self.board, 7, Board.X, "---|-XO|---")
