from mock import patch
from test_td_learning_player import TestTDLearningPlayer
from td_symmetric_learning_player import TDSymmetricLearningPlayer
from board import Board
from board_test_utils import get_board_state_tuple, assert_get_move_is, set_board
from mock_random import MockRandom

class TestTDSymmetricLearningPlayer(TestTDLearningPlayer):
    def setUp(self):
        super().setUp()
        self.player = TDSymmetricLearningPlayer()
        self.file_name_prefix = "TDSymmetricLearningPlayer"
        self.player.set_board(self.board)
        self.player.enable_learning()

    def assert_get_value_and_state_symmetric_is(self, value, pieces, symmetric_pieces, winner, piece):
        self.player.set_piece(piece)
        state = get_board_state_tuple(pieces)
        symmetric_state = get_board_state_tuple(symmetric_pieces)
        current_value, new_state = self.player._get_value_and_state(symmetric_state, winner)
        self.assertAlmostEqual(value, current_value)
        self.assertEqual(state, new_state)
        self.assertIn(state, self.player.values)
        if symmetric_state != state:
            self.assertNotIn(symmetric_state, self.player.values)

    def assert_values_after_reward_symmetric_are(self, values, pieces_list, symmetric_pieces_list, winner):
        self.player.set_piece(Board.X)
        values_dict = {}
        for pieces, symmetric_pieces, value in zip(pieces_list, symmetric_pieces_list, values):
            set_board(self.board, symmetric_pieces)
            self.player.store_state()
            values_dict[get_board_state_tuple(pieces)] = value
        self.player.set_reward(winner)
        self.assertEqual(sorted(values_dict.keys()), sorted(self.player.values.keys()))
        for key, value in self.player.values.items():
            self.assertAlmostEqual(self.player.values[key], value)

    def test_get_value_and_state_returns_current_value_if_symmetric_state_known(self):
        state1 = get_board_state_tuple("XO-|X--|---")
        state2 = get_board_state_tuple("XO-|X--|O--")
        self.player.values[state1] = 0.56
        self.player.values[state2] = 0.45

        # Original
        self.assert_get_value_and_state_symmetric_is(0.56, "XO-|X--|---", "XO-|X--|---", None, Board.X)
        self.assert_get_value_and_state_symmetric_is(0.45, "XO-|X--|O--", "XO-|X--|O--", None, Board.O)

        # Rotated by 90 degrees
        self.assert_get_value_and_state_symmetric_is(0.56, "XO-|X--|---", "---|O--|XX-", None, Board.X)
        self.assert_get_value_and_state_symmetric_is(0.45, "XO-|X--|O--", "---|O--|XXO", None, Board.O)

        # Rotated by 180 degrees
        self.assert_get_value_and_state_symmetric_is(0.56, "XO-|X--|---", "---|--X|-OX", None, Board.X)
        self.assert_get_value_and_state_symmetric_is(0.45, "XO-|X--|O--", "--O|--X|-OX", None, Board.O)

        # Rotated by 270 degrees
        self.assert_get_value_and_state_symmetric_is(0.56, "XO-|X--|---", "-XX|--O|---", None, Board.X)
        self.assert_get_value_and_state_symmetric_is(0.45, "XO-|X--|O--", "OXX|--O|---", None, Board.O)

        # Reflected horizontally
        self.assert_get_value_and_state_symmetric_is(0.56, "XO-|X--|---", "---|X--|XO-", None, Board.X)
        self.assert_get_value_and_state_symmetric_is(0.45, "XO-|X--|O--", "O--|X--|XO-", None, Board.O)

        # Reflected vertically
        self.assert_get_value_and_state_symmetric_is(0.56, "XO-|X--|---", "-OX|--X|---", None, Board.X)
        self.assert_get_value_and_state_symmetric_is(0.45, "XO-|X--|O--", "-OX|--X|--O", None, Board.O)

         # Reflected on left diagonal
        self.assert_get_value_and_state_symmetric_is(0.56, "XO-|X--|---", "XX-|O--|---", None, Board.X)
        self.assert_get_value_and_state_symmetric_is(0.45, "XO-|X--|O--", "XXO|O--|---", None, Board.O)
        
         # Reflected on right diagonal
        self.assert_get_value_and_state_symmetric_is(0.56, "XO-|X--|---", "---|--O|-XX", None, Board.X)
        self.assert_get_value_and_state_symmetric_is(0.45, "XO-|X--|O--", "---|--O|OXX", None, Board.O)

    @patch('td_learning_player.random.choice')
    @patch('td_learning_player.random.random')
    def test_get_move_chooses_best_available_move_if_random_gte_epsilon(
            self, random_mock, choice_mock):
        random_mock.return_value = 0.1
        choice_mock.side_effect = MockRandom(0).choice
        self.player.values[get_board_state_tuple("---|-XO|---")] = 0.501 # Original
                                                                         # Reflected horizontally
        
        # Force other symmetric choices to be of lower value
        self.player.values[get_board_state_tuple("-O-|-X-|---")] = 0.499 # Rotated by 90 degrees
                                                                         # Reflected on right diagonal
        self.player.values[get_board_state_tuple("---|OX-|---")] = 0.499 # Rotated by 180 degrees
                                                                         # Reflected vertically
        self.player.values[get_board_state_tuple("---|-X-|-O-")] = 0.499 # Rotated by 270 degrees
                                                                         # Reflected on left diagonal

        assert_get_move_is(self, self.player, self.board, 5, Board.O, "---|-X-|---")
        choice_mock.assert_called_once_with([5])

    @patch('td_learning_player.random.choice')
    @patch('td_learning_player.random.random')
    def test_get_move_chooses_random_best_available_move_if_random_gte_epsilon_and_multiple_bests(
            self, random_mock, choice_mock):
        random_mock.return_value = 0.1
        choice_mock.side_effect = MockRandom(1).choice

        self.player.values[get_board_state_tuple("X--|-XO|---")] = 0.501 # position 0
        self.player.values[get_board_state_tuple("--X|-XO|---")] = 0.501 # position 2

        # Symmetries for X--|-XO|---:
        #                -O-|-X-|X-- (Rotated by 90 degrees)
        #                ---|OX-|--X (Rotated by 180 degrees)
        #                --X|-X-|-O- (Rotated by 270 degrees)
        #                ---|-XO|X-- (Reflected horizontally) - position 6
        #                --X|OX-|--- (Reflected vertically)
        #                X--|-X-|-O- (Reflected on left diagonal)
        #                -O-|-X-|--X (Reflected on right diagonal)
        #
        # Symmetries for --X|-XO|---:
        #                XO-|-X-|--- (Rotated by 90 degrees)
        #                ---|OX-|X-- (Rotated by 180 degrees)
        #                ---|-X-|-OX (Rotated by 270 degrees)
        #                ---|-XO|--X (Reflected horizontally) - position 8
        #                X--|OX-|--- (Reflected vertically)
        #                ---|-X-|XO- (Reflected on left diagonal)
        #                -OX|-X-|--- (Reflected on right diagonal)

        assert_get_move_is(self, self.player, self.board, 2, Board.X, "---|-XO|---")
        choice_mock.assert_called_once_with([0, 2, 6, 8])

    def test_set_reward_updates_values_for_each_symmetric_state(self):
        self.player.set_params(alpha=0.4)
        
        # Original
        self.assert_values_after_reward_symmetric_are(
            [0.5128, 0.532, 0.58, 0.7, 1.0],
            ["X--|---|---",
             "XO-|---|---",
             "XO-|X--|---",
             "XO-|XO-|---",
             "XO-|XO-|X--"],
            ["X--|---|---",
             "XO-|---|---",
             "XO-|X--|---",
             "XO-|XO-|---",
             "XO-|XO-|X--"],
            Board.X)

        # Rotated by 90 degrees
        self.assert_values_after_reward_symmetric_are(
            [0.54352, 0.5896, 0.676, 0.82, 1.0],
            ["X--|---|---",
             "XO-|---|---",
             "XO-|X--|---",
             "XO-|XO-|---",
             "XO-|XO-|X--"],
            ["---|O--|X--",
             "---|O--|X--",
             "---|O--|XX-",
             "---|OO-|XX-",
             "---|OO-|XXX"],
            Board.X)

        # Rotated by 180 degrees
        self.assert_values_after_reward_symmetric_are(
            [0.5896, 0.65872, 0.7624, 0.892, 1.0],
            ["X--|---|---",
             "XO-|---|---",
             "XO-|X--|---",
             "XO-|XO-|---",
             "XO-|XO-|X--"],
            ["---|---|--X",
             "---|---|-OX",
             "---|--X|-OX",
             "---|-OX|-OX",
             "--X|-OX|-OX"],
            Board.X)

        # Rotated by 270 degrees
        self.assert_values_after_reward_symmetric_are(
            [0.644896, 0.72784, 0.83152, 0.9352, 1.0],
            ["X--|---|---",
             "XO-|---|---",
             "XO-|X--|---",
             "XO-|XO-|---",
             "XO-|XO-|X--"],
            ["--X|---|---",
             "--X|--O|---",
             "-XX|--O|---",
             "-XX|-OO|---",
             "XXX|-OO|---"],
            Board.X)

        # Reflected horizontally
        self.assert_values_after_reward_symmetric_are(
            [0.7029568, 0.790048, 0.88336, 0.96112, 1.0],
            ["X--|---|---",
             "XO-|---|---",
             "XO-|X--|---",
             "XO-|XO-|---",
             "XO-|XO-|X--"],
            ["---|---|X--",
             "---|---|XO-",
             "---|X--|XO-",
             "---|XO-|XO-",
             "X--|XO-|XO-"],
            Board.X)

        # Reflected vertically
        self.assert_values_after_reward_symmetric_are(
            [0.7586952, 0.8423027, 0.9206848, 0.976672, 1.0],
            ["X--|---|---",
             "XO-|---|---",
             "XO-|X--|---",
             "XO-|XO-|---",
             "XO-|XO-|X--"],
            ["--X|---|---",
             "-OX|---|---",
             "-OX|--X|---",
             "-OX|-OX|---",
             "-OX|-OX|--X"],
            Board.X)

        # Reflected on left diagonal
        self.assert_values_after_reward_symmetric_are(
            [0.8088597, 0.8841065, 0.9468122, 0.9860032, 1.0],
            ["X--|---|---",
             "XO-|---|---",
             "XO-|X--|---",
             "XO-|XO-|---",
             "XO-|XO-|X--"],
            ["X--|---|---",
             "X--|O--|---",
             "XX-|O--|---",
             "XX-|OO-|---",
             "XXX|OO-|---"],
            Board.X)

        # Reflected on right diagonal
        self.assert_values_after_reward_symmetric_are(
            [0.8518579, 0.9163551, 0.9647281, 0.9916019, 1.0],
            ["X--|---|---",
             "XO-|---|---",
             "XO-|X--|---",
             "XO-|XO-|---",
             "XO-|XO-|X--"],
            ["---|---|--X",
             "---|--O|--X",
             "---|--O|-XX",
             "---|-OO|-XX",
             "---|-OO|XXX"],
            Board.X)
