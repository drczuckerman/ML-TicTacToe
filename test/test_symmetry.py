import unittest
from symmetry import Symmetry
from board import Board
from board_test_utils import set_board, assert_board_state_tuple_is

class test_symmetry(unittest.TestCase):
    def setUp(self):
        self.symmetry = Symmetry()

    def assert_symmetry_is(self, num_skip, pieces, expected_pieces):
        board = Board()
        set_board(board, pieces)
        state_generator = self.symmetry.get_symmetries(board.state)
        for _ in range(num_skip + 1):
            symmetric_state = next(state_generator)
        assert_board_state_tuple_is(self, expected_pieces, symmetric_state)

    def test_get_symmetry_original(self):
        self.assert_symmetry_is(0, "XO-|-XO|OX-", "XO-|-XO|OX-")

    def test_get_symmetry_rotate_by_90_degrees(self):
        self.assert_symmetry_is(1, "XO-|-XO|OX-", "-O-|OXX|X-O")

    def test_get_symmetry_rotate_by_180_degrees(self):
        self.assert_symmetry_is(2, "XO-|-XO|OX-", "-XO|OX-|-OX")

    def test_get_symmetry_rotate_by_270_degrees(self):
        self.assert_symmetry_is(3, "XO-|-XO|OX-", "O-X|XXO|-O-")

    def test_get_symmetry_reflect_horizontally(self):
        self.assert_symmetry_is(4, "XO-|-XO|OX-", "OX-|-XO|XO-")

    def test_get_symmetry_reflect_vertically(self):
        self.assert_symmetry_is(5, "XO-|-XO|OX-", "-OX|OX-|-XO")

    def test_get_symmetry_reflect_left_diagonal(self):
        self.assert_symmetry_is(6, "XO-|-XO|OX-", "X-O|OXX|-O-")

    def test_get_symmetry_reflect_right_diagonal(self):
        self.assert_symmetry_is(7, "XO-|-XO|OX-", "-O-|XXO|O-X")
