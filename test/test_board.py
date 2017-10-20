import unittest
from board import Board
from board_test_utils import (set_board, assert_board_is, get_index_and_pieces, 
                              get_expected_formatted_board, assert_board_state_tuple_is)

class TestBoard(unittest.TestCase):
    def setUp(self):
        self.board = Board()

    def assert_move_is_invalid(self, position, pieces=""):
        self.assert_move_is(False, position, pieces)

    def assert_move_is_valid(self, position, pieces=""):
        self.assert_move_is(True, position, pieces)

    def assert_move_is(self, valid, position, pieces=""):
        set_board(self.board, pieces)
        self.assertEqual(valid, self.board.is_valid_move(position))

    def assert_board_is_after_move(self, pieces, position, piece):
        self.board.make_move(position, piece)
        assert_board_is(self, self.board, pieces)

    def assert_get_available_moves_are(self, positions, pieces=""):
        set_board(self.board, pieces)
        self.assertEqual(positions, self.board.get_available_moves())

    def assert_winning_positions_are(self, positions, pieces=""):
        set_board(self.board, pieces)
        self.assertEqual(positions, self.board.get_winning_positions())

    def assert_winner_is(self, winner, pieces=""):
        set_board(self.board, pieces)
        self.assertEqual(winner, self.board.get_winner())
        
    def assert_try_move_is(self, expected_winner, pieces_before, pieces_after, position, piece):
        set_board(self.board, pieces_before)
        with self.board.try_move(position, piece) as (winner, state):
            self.assertEqual(expected_winner, winner)
            assert_board_is(self, self.board, pieces_after)
            assert_board_state_tuple_is(self, pieces_after, state)
        assert_board_is(self, self.board, pieces_before)

    def assert_board_format_is(self, formatted_pieces, pieces=""):
        set_board(self.board, pieces)
        self.assertEqual(get_expected_formatted_board(formatted_pieces), self.board.format_board())

    def test_constructor(self):
        assert_board_is(self, self.board)

    def test_is_invalid_move_returns_false_if_invalid_move(self):
        self.assert_move_is_invalid(-1)
        self.assert_move_is_invalid(9)

    def test_is_valid_move_returns_false_when_position_taken(self):
        for position in range(9):
            self.assert_move_is_invalid(position, pieces="XOX|OXO|XOX")

    def test_is_valid_move_returns_true_when_position_not_taken(self):
        for position in range(9):
            self.assert_move_is_valid(position)

    def test_make_move(self):
        self.assert_board_is_after_move("X--|---|---", 0, Board.X)
        self.assert_board_is_after_move("XO-|---|---", 1, Board.O)
        self.assert_board_is_after_move("XOX|---|---", 2, Board.X)
        self.assert_board_is_after_move("XOX|O--|---", 3, Board.O)
        self.assert_board_is_after_move("XOX|OX-|---", 4, Board.X)
        self.assert_board_is_after_move("XOX|OXO|---", 5, Board.O)
        self.assert_board_is_after_move("XOX|OXO|X--", 6, Board.X)
        self.assert_board_is_after_move("XOX|OXO|XO-", 7, Board.O)
        self.assert_board_is_after_move("XOX|OXO|XOX", 8, Board.X)

    def test_get_available_moves_returns_all_moves_if_empty(self):
        self.assert_get_available_moves_are(list(range(9)))

    def test_get_available_moves_returns_available_moves_if_not_empty(self):
        self.assert_get_available_moves_are([1,3,5,7], "X-O|-X-|X-O")
        self.assert_get_available_moves_are([0,2,4,6,8], "-X-|O-O|-X-")

    def test_get_available_moves_returns_no_moves_if_full(self):
        self.assert_get_available_moves_are([], "XXO|OXX|XOO")

    def test_get_winning_positions_returns_nothing_if_no_win(self):
        self.assert_winning_positions_are([],"XOX|OXX|OXO")

    def test_get_winning_positions_returns_positions_if_three_in_row_horiz(self):
        self.assert_winning_positions_are([0,1,2], "XXX|---|---")
        self.assert_winning_positions_are([0,1,2], "OOO|---|---")

        self.assert_winning_positions_are([3,4,5], "---|XXX|---")
        self.assert_winning_positions_are([3,4,5], "---|OOO|---")

        self.assert_winning_positions_are([6,7,8], "---|---|XXX")
        self.assert_winning_positions_are([6,7,8], "---|---|OOO")

    def test_get_winning_positions_returns_positions_if_three_in_row_vert(self):
        self.assert_winning_positions_are([0,3,6], "X--|X--|X--")
        self.assert_winning_positions_are([0,3,6], "O--|O--|O--")

        self.assert_winning_positions_are([1,4,7], "-X-|-X-|-X-")
        self.assert_winning_positions_are([1,4,7], "-O-|-O-|-O-")

        self.assert_winning_positions_are([2,5,8], "--X|--X|--X")
        self.assert_winning_positions_are([2,5,8], "--O|--O|--O")

    def test_get_winning_positions_returns_positions_if_three_in_row_diag(self):
        self.assert_winning_positions_are([0,4,8], "X--|-X-|--X")
        self.assert_winning_positions_are([0,4,8], "O--|-O-|--O")

        self.assert_winning_positions_are([2,4,6], "--X|-X-|X--")
        self.assert_winning_positions_are([2,4,6], "--O|-O-|O--")

    def test_get_winner_indicates_no_winner_if_empty_board(self):
        self.assert_winner_is(None)

    def test_get_winner_indicates_no_winner_if_one_in_row(self):
        self.assert_winner_is(None, "X--|---|---")
        self.assert_winner_is(None, "O--|---|---")

        self.assert_winner_is(None, "-X-|---|---")
        self.assert_winner_is(None, "-O-|---|---")

        self.assert_winner_is(None, "--X|---|---")
        self.assert_winner_is(None, "--O|---|---")

        self.assert_winner_is(None, "---|X--|---")
        self.assert_winner_is(None, "---|O--|---")

        self.assert_winner_is(None, "---|-X-|---")
        self.assert_winner_is(None, "---|-O-|---")

        self.assert_winner_is(None, "---|--X|---")
        self.assert_winner_is(None, "---|--O|---")

        self.assert_winner_is(None, "---|---|X--")
        self.assert_winner_is(None, "---|---|O--")

        self.assert_winner_is(None, "---|---|-X-")
        self.assert_winner_is(None, "---|---|-O-")

        self.assert_winner_is(None, "---|---|--X")
        self.assert_winner_is(None, "---|---|--O")

    def test_get_winner_indicates_no_winner_if_two_in_row_horiz(self):
        self.assert_winner_is(None, "XXO|------")
        self.assert_winner_is(None, "XOX|------")
        self.assert_winner_is(None, "OXX|------")
        self.assert_winner_is(None, "OOX|------")
        self.assert_winner_is(None, "OXO|------")
        self.assert_winner_is(None, "XOO|------")

        self.assert_winner_is(None, "---|XXO---")
        self.assert_winner_is(None, "---|XOX---")
        self.assert_winner_is(None, "---|OXX---")
        self.assert_winner_is(None, "---|OOX---")
        self.assert_winner_is(None, "---|OXO---")
        self.assert_winner_is(None, "---|XOO---")

        self.assert_winner_is(None, "---|---|XXO")
        self.assert_winner_is(None, "---|---|XOX")
        self.assert_winner_is(None, "---|---|OXX")
        self.assert_winner_is(None, "---|---|OOX")
        self.assert_winner_is(None, "---|---|OXO")
        self.assert_winner_is(None, "---|---|XOO")

    def test_get_winner_indicates_no_winner_if_two_in_row_horiz(self):
        self.assert_winner_is(None, "X--|X--|O--")
        self.assert_winner_is(None, "X--|O--|X--")
        self.assert_winner_is(None, "O--|X--|X--")
        self.assert_winner_is(None, "O--|O--|X--")
        self.assert_winner_is(None, "O--|X--|O--")
        self.assert_winner_is(None, "X--|O--|O--")

        self.assert_winner_is(None, "-X-|-X-|-O-")
        self.assert_winner_is(None, "-X-|-O-|-X-")
        self.assert_winner_is(None, "-O-|-X-|-X-")
        self.assert_winner_is(None, "-O-|-O-|-X-")
        self.assert_winner_is(None, "-O-|-X-|-O-")
        self.assert_winner_is(None, "-X-|-O-|-O-")

        self.assert_winner_is(None, "--X|--X|--O")
        self.assert_winner_is(None, "--X|--O|--X")
        self.assert_winner_is(None, "--O|--X|--X")
        self.assert_winner_is(None, "--O|--O|--X")
        self.assert_winner_is(None, "--O|--X|--O")
        self.assert_winner_is(None, "--X|--O|--O")

    def test_get_winner_indicates_no_winner_if_two_in_row_diag(self):
        self.assert_winner_is(None, "X--|-X-|--O")
        self.assert_winner_is(None, "X--|-O-|--X")
        self.assert_winner_is(None, "O--|-X-|--X")
        self.assert_winner_is(None, "O--|-O-|--X")
        self.assert_winner_is(None, "O--|-X-|--O")
        self.assert_winner_is(None, "X--|-O-|--O")

        self.assert_winner_is(None, "--X|-X-|O--")
        self.assert_winner_is(None, "--X|-O-|X--")
        self.assert_winner_is(None, "--O|-X-|X--")
        self.assert_winner_is(None, "--O|-O-|X--")
        self.assert_winner_is(None, "--O|-X-|O--")
        self.assert_winner_is(None, "--X|-O-|O--")

    def test_get_winner_indicate_winner_if_three_in_row_horiz(self):
        self.assert_winner_is(Board.X, "XXX|---|---")
        self.assert_winner_is(Board.X, "---|XXX|---")
        self.assert_winner_is(Board.X, "---|---|XXX")

        self.assert_winner_is(Board.O, "OOO|---|---")
        self.assert_winner_is(Board.O, "---|OOO|---")
        self.assert_winner_is(Board.O, "---|---|OOO")

    def test_get_winner_indicate_winner_if_three_in_row_vert(self):
        self.assert_winner_is(Board.X, "X--|X--|X--")
        self.assert_winner_is(Board.X, "-X-|-X-|-X-")
        self.assert_winner_is(Board.X, "--X|--X|--X")

        self.assert_winner_is(Board.O, "O--|O--|O--")
        self.assert_winner_is(Board.O, "-O-|-O-|-O-")
        self.assert_winner_is(Board.O, "--O|--O|--O")

    def test_get_winner_indicates_no_winner_if_three_in_row_diag(self):
        self.assert_winner_is(Board.X, "X--|-X-|--X")
        self.assert_winner_is(Board.X, "--X|-X-|X--")

        self.assert_winner_is(Board.O, "O--|-O-|--O")
        self.assert_winner_is(Board.O, "--O|-O-|O--")

    def test_get_winner_indicates_draw_if_no_winner_and_board_full(self):
        self.assert_winner_is(Board.DRAW, "XOX|XOO|OXX")
        self.assert_winner_is(Board.DRAW, "XXO|OXX|XOO")

    def test_is_valid_move_returns_false_if_game_over(self):
        self.assert_move_is_invalid(8, "-XO|-XO|-X-")
        
    def test_try_move_indicates_no_winner_if_no_winner(self):
        self.assert_try_move_is(None, "XO-|---|---", "XOX|---|---", 2, Board.X)

    def test_try_move_indicates_x_wins_when_x_wins(self):
        self.assert_try_move_is(Board.X, "X-O|XO-|---", "X-O|XO-|X--", 6, Board.X)

    def test_try_move_indicates_o_wins_when_o_wins(self):
        self.assert_try_move_is(Board.O, "--O|X-X|OX-", "--O|XOX|OX-", 4, Board.O)
        
    def test_try_move_indicates_draw_when_draw(self):
        self.assert_try_move_is(Board.DRAW, "OXO|XXO|OO-", "OXO|XXO|OOX", 8, Board.X)

    def test_get_winner_text(self):
        self.assertEqual(None, Board.get_winner_text(None))
        self.assertEqual("X Wins", Board.get_winner_text(Board.X))
        self.assertEqual("O Wins", Board.get_winner_text(Board.O))
        self.assertEqual("Draw", Board.get_winner_text(Board.DRAW))

    def test_format_piece(self):
        self.assertEqual("X", Board.format_piece(Board.X))
        self.assertEqual("O", Board.format_piece(Board.O))

    def test_format_board_shows_numbers_for_empty_cells(self):
        self.assert_board_format_is(formatted_pieces="---|---|---")

    def test_format_board_shows_pieces_for_non_empty_cells_and_numbers_for_empty_cells(self):
        self.assert_board_format_is(formatted_pieces="x--|o-x|-o-", pieces="X--|O-X|-O-")

    def test_format_board_shows_pieces_for_non_empty_cells(self):
        self.assert_board_format_is(formatted_pieces="oxo|xxo|oox", pieces="OXO|XXO|OOX")

    def test_format_board_shows_winning_positions_for_three_in_row_horiz(self):
        self.assert_board_format_is(formatted_pieces="XXX|xoo|oo-", pieces="XXX|XOO|OO-")
        self.assert_board_format_is(formatted_pieces="x-x|OOO|oxx", pieces="X-X|OOO|OXX")

    def test_format_board_shows_winning_positions_for_three_in_row_vert(self):
        self.assert_board_format_is(formatted_pieces="-X-|oXo|oX-", pieces="-X-|OXO|OX-")
        self.assert_board_format_is(formatted_pieces="x-O|xxO|-xO", pieces="X-O|XXO|-XO")

    def test_format_board_shows_winning_positions_for_three_in_row_diag(self):
        self.assert_board_format_is(formatted_pieces="X--|oX-|o-X", pieces="X--|OX-|O-X")
        self.assert_board_format_is(formatted_pieces="--O|xOx|Ox-", pieces="--O|XOX|OX-")
