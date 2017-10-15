import unittest
from mock import patch, call
from io import StringIO
from board import Board
from human_player import HumanPlayer
from board_test_utils import set_board

class TestHumanPlayer(unittest.TestCase):
    def setUp(self):
        self.player = HumanPlayer()
        self.board = Board()
        self.player.set_board(self.board)
        self.player.set_piece(Board.X)

    def test_constructor_initializes_board(self):
        player = HumanPlayer()
        self.assertIsNone(player.board)

    def test_constructor_initializes_piece(self):
        player = HumanPlayer()
        self.assertIsNone(player.piece)

    def test_set_board(self):
        self.assertEqual(self.board, self.player.board)

    def test_set_piece(self):
        player1 = HumanPlayer()
        player1.set_piece(Board.X)
        self.assertEqual(Board.X, player1.piece)

        player2 = HumanPlayer()
        player2.set_piece(Board.O)
        self.assertEqual(Board.O, player2.piece)

    @patch('sys.stdout', new_callable=StringIO)
    @patch('builtins.input')
    def test_get_move_for_valid_move(self, input_mock, stdout_mock):
        input_mock.return_value = "5"
        self.assertEqual(4, self.player.get_move())
        input_mock.assert_called_once_with("Enter move: ")
        self.assertEqual("", stdout_mock.getvalue())

    @patch('sys.stdout', new_callable=StringIO)
    @patch('builtins.input')
    def test_get_move_for_invalid_input(self, input_mock, stdout_mock):
        input_mock.side_effect = ["X", " 6 "]
        self.assertEqual(5, self.player.get_move())
        self.assertEqual([call("Enter move: ")]*2, input_mock.call_args_list)
        self.assertEqual("Invalid input\n", stdout_mock.getvalue())

    @patch('sys.stdout', new_callable=StringIO)
    @patch('builtins.input')
    def test_get_move_for_invalid_move(self, input_mock, stdout_mock):
        set_board(self.board, "XO-|---|---")
        input_mock.side_effect = ["1", "2", "3"]
        self.assertEqual(2, self.player.get_move())
        self.assertEqual([call("Enter move: ")]*3, input_mock.call_args_list)
        self.assertEqual("Invalid move\nInvalid move\n", stdout_mock.getvalue())
