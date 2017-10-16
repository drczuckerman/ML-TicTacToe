import unittest
from mock import patch
from game_controller import GameController
from board import Board
from player import Player
from learning_computer_player import LearningComputerPlayer
from board_test_utils import assert_board_is, set_board

class MockPlayer(Player):
    def __init__(self):
        super().__init__()
        self.index = 0
        self.positions = []

    def set_moves(self, positions):
        self.positions = positions
 
    def get_move(self):
        position = self.positions[self.index]
        self.index += 1
        return position

class MockLearningComputerPlayer(LearningComputerPlayer):
    def __init__(self):
        super().__init__()
        self.reset_called = False

    def reset(self):
        super().reset()
        self.reset_called = True

class TestGameController(unittest.TestCase):
    def setUp(self):
        self.player1 = MockPlayer()
        self.player2 = MockPlayer()
        self.controller = GameController(self.player1, self.player2)

    def assert_player_is(self, player_number, player):
        self.controller.player_number = player_number
        self.assertEqual(player, self.controller.get_player())

    def assert_make_moves_winner_is(self, winner, positions):
        self.player1.set_moves(positions[0::2])
        self.player2.set_moves(positions[1::2])

        for position in positions[:-1]:
            self.assertEqual((None, position), self.controller.make_move())
        self.assertEqual((winner, positions[-1]), self.controller.make_move())

    def test_constructor_stores_players(self):
        self.assertEqual([self.player1, self.player2], self.controller.players)

    def test_constructor_initializes_board(self):
        self.assertEqual(list(range(9)), self.controller.board.get_available_moves())

    def test_constructor_resets_player_number(self):
        self.assertEqual(0, self.controller.player_number)

    def test_constructor_stores_board_for_each_player(self):
        self.assertEqual(self.controller.board, self.player1.board)
        self.assertEqual(self.controller.board, self.player2.board)

    def test_constructor_stores_pieces_for_each_player(self):
        self.assertEqual(Board.X, self.player1.piece)
        self.assertEqual(Board.O, self.player2.piece)

    def test_constructor_resets_learning_player(self):
        player1 = MockLearningComputerPlayer()
        player2 = MockLearningComputerPlayer()
        controller = GameController(player1, player2)
        self.assertTrue(player1.reset_called)
        self.assertTrue(player2.reset_called)

    def test_get_player(self):
        self.assert_player_is(0, self.player1)
        self.assert_player_is(1, self.player2)
        
    def test_make_move_sets_board_and_changes_player_number_when_valid_move(self):
        self.player1.set_moves([4])
        self.assertEqual((None, 4), self.controller.make_move())
        assert_board_is(self, self.controller.board, "---|-X-|---")
        self.assertEqual(1, self.controller.player_number)

    def test_make_move_indicates_winner_when_x_wins(self):
        self.assert_make_moves_winner_is(Board.X, [6, 2, 8, 1, 7])
        assert_board_is(self, self.controller.board, "-OO|---|XXX")
 
    def test_make_move_indicates_winner_when_o_wins(self):
        self.assert_make_moves_winner_is(Board.O, [0, 2, 1, 4, 3, 6])
        assert_board_is(self, self.controller.board, "XXO|XO-|O--")

    def test_make_move_indicates_draw_when_board_full(self):
        self.assert_make_moves_winner_is(Board.DRAW, [4, 0, 6, 2, 1, 7, 5, 3, 8])
        assert_board_is(self, self.controller.board, "OXO|OXX|XOX")
