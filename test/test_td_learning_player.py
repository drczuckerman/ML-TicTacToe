import unittest
import random
from mock import patch
from td_learning_player import TDLearningPlayer
from board import Board
from board_test_utils import get_board_state_tuple, set_board

class MockRandom(object):
    def __init__(self, choice_index):
        self.choice_index = choice_index

    def choice(self, choices):
        return choices[self.choice_index]

class TestTdLearningPlayer(unittest.TestCase):
    def setUp(self):
        self.player = TDLearningPlayer()
        self.board = Board()
        self.player.set_board(self.board)
        self.player.set_params()

    def assert_stored_states_are(self, pieces_list, position, piece):
        self.board.make_move(position, piece)
        self.player.store_state()
        states = list(map(get_board_state_tuple, pieces_list))
        self.assertEqual(self.player.states, states)

    def assert_get_reward_is(self, reward, winner, piece):
        self.player.set_piece(piece)
        self.assertAlmostEqual(reward, self.player._get_reward(winner))
        
    def assert_get_value_is(self, value, pieces, winner, piece):
        self.player.set_piece(piece)
        state = get_board_state_tuple(pieces)
        self.assertAlmostEqual(value, self.player._get_value(state, winner))
        self.assertIn(state, self.player.values)
        
    def assert_values_after_reward_are(self, values, pieces_list, winner):
        self.player.set_piece(Board.X)
        values_dict = {}
        for pieces, value in zip(pieces_list, values):
            set_board(self.board, pieces)
            self.player.store_state()
            values_dict[get_board_state_tuple(pieces)] = value
        self.player.set_reward(winner)
        self.assertEqual(values_dict, self.player.values)

    def assert_get_move_is(self, position, piece, pieces=""):
        self.player.set_piece(piece)
        set_board(self.board, pieces)
        self.assertEqual(position, self.player.get_move())

    def test_constructor_initializes_board_and_piece_to_none(self):
        player = TDLearningPlayer()
        self.assertIsNone(player.piece)
        self.assertIsNone(player.board)

    def test_constructor_initializes_empty_values(self):
        self.assertEqual({}, self.player.values)
        
    def test_constructor_initialize_stored_states(self):
        self.assertEqual([], self.player.states)

    def test_set_board(self):
        self.assertEqual(self.board, self.player.board)

    def test_set_piece(self):
        player1 = TDLearningPlayer()
        player1.set_piece(Board.X)
        self.assertEqual(Board.X, player1.piece)

        player2 = TDLearningPlayer()
        player2.set_piece(Board.O)
        self.assertEqual(Board.O, player2.piece)

    def test_set_params_sets_default_alpha_if_not_specified(self):
        self.player.set_params()
        self.assertAlmostEqual(0.5, self.player.alpha)

    def test_set_params_sets_alpha_if_specified(self):
        self.player.set_params(alpha=0.1)
        self.assertAlmostEqual(0.1, self.player.alpha)

    def test_set_params_sets_default_epsilon_if_not_specified(self):
        self.player.set_params()
        self.assertAlmostEqual(0.1, self.player.epsilon)

    def test_set_params_sets_epsilon_if_specified(self):
        self.player.set_params(epsilon=0.4)
        self.assertAlmostEqual(0.4, self.player.epsilon)

    def test_set_params_sets_default_draw_rewards_if_not_specified(self):
        self.player.set_params()
        self.assertAlmostEqual(0.5, self.player.draw_rewards[Board.X])
        self.assertAlmostEqual(0.5, self.player.draw_rewards[Board.O])

    def test_set_params_sets_specified_x_reward_if_specified(self):
        self.player.set_params(x_draw_reward=0.4)
        self.assertAlmostEqual(0.4, self.player.draw_rewards[Board.X])
        self.assertAlmostEqual(0.5, self.player.draw_rewards[Board.O])

    def test_set_params_sets_specified_o_reward_if_specified(self):
        self.player.set_params(o_draw_reward=0.6)
        self.assertAlmostEqual(0.5, self.player.draw_rewards[Board.X])
        self.assertAlmostEqual(0.6, self.player.draw_rewards[Board.O])

    def test_set_params_sets_specified_x_and_o_reward_if_specified(self):
        self.player.set_params(x_draw_reward=0.44, o_draw_reward=0.56)
        self.assertAlmostEqual(0.44, self.player.draw_rewards[Board.X])
        self.assertAlmostEqual(0.56, self.player.draw_rewards[Board.O])

    def test_store_state_appends_state(self):
        self.assert_stored_states_are(["X--|---|---"], 0, Board.X)
        self.assert_stored_states_are(["X--|---|---", "XO-|---|---"], 1, Board.O)
        self.assert_stored_states_are(["X--|---|---", "XO-|---|---", "XOX|---|---"], 2, Board.X)
        
    def test_get_reward_returns_1_if_winner_is_same_as_piece(self):
        self.assert_get_reward_is(1.0, Board.X, Board.X)
        self.assert_get_reward_is(1.0, Board.O, Board.O)

    def test_get_reward_returns_0_if_winner_is_opposite_of_piece(self):
        self.assert_get_reward_is(0.0, Board.O, Board.X)
        self.assert_get_reward_is(0.0, Board.X, Board.O)

    def test_get_reward_returns_draw_reward_if_winner_is_draw(self):
        self.player.set_params(x_draw_reward=0.48, o_draw_reward=0.52)
        self.assert_get_reward_is(0.48, Board.DRAW, Board.X)
        self.assert_get_reward_is(0.52, Board.DRAW, Board.O)

    def test_get_value_returns_0_5_if_non_ending_state_not_stored(self):
        self.assert_get_value_is(0.5, "X--|---|---", None, Board.X)

    def test_get_value_returns_1_if_winning_state(self):
        self.assert_get_value_is(1.0, "O-O|XXX|---", Board.X, Board.X)
        self.assert_get_value_is(1.0, "OX-|O-X|OX-", Board.O, Board.O)

    def test_get_value_returns_0_if_losing_state(self):
        self.assert_get_value_is(0.0, "XOX|-O-|XO-", Board.O, Board.X)
        self.assert_get_value_is(0.0, "--X|OX-|XO-", Board.X, Board.O)

    def test_get_value_returns_draw_reward_if_draw_state(self):
        self.player.set_params(x_draw_reward=0.3, o_draw_reward=0.7)
        self.assert_get_value_is(0.3, "XXO|OOX|XOX", Board.DRAW, Board.X)
        self.assert_get_value_is(0.7, "OOX|XXO|OXO", Board.DRAW, Board.O)

    def test_get_value_returns_current_value_if_state_known(self):
        state1 = get_board_state_tuple("X--|---|---")
        state2 = get_board_state_tuple("XO-|---|---")
        self.player.values[state1] = 0.6
        self.player.values[state2] = 0.3
        self.assert_get_value_is(0.6, "X--|---|---", None, Board.X)
        self.assert_get_value_is(0.3, "XO-|---|---", None, Board.O)

    def test_set_reward_updates_values_for_each_state(self):
        self.player.set_params(alpha=0.4)
        self.assert_values_after_reward_are(
            [0.5128, 0.532, 0.58, 0.7, 1.0],
            ["X--|---|---",
             "XO-|---|---",
             "XO-|X--|---",
             "XO-|XO-|---",
             "XO-|XO-|X--"],
            Board.X)

    @patch('td_learning_player.random.choice')
    @patch('td_learning_player.random.random')
    def test_get_move_chooses_random_available_move_if_random_lt_epsilon(
            self, random_mock, choice_mock):
        random_mock.return_value = 0.099
        choice_mock.side_effect = MockRandom(4).choice
        self.assert_get_move_is(6, Board.X, "X--|-O-|---")
        choice_mock.assert_called_once_with([1, 2, 3, 5, 6, 7, 8])

    @patch('td_learning_player.random.choice')
    @patch('td_learning_player.random.random')
    def test_get_move_chooses_best_available_move_if_random_gte_epsilon(
            self, random_mock, choice_mock):
        random_mock.return_value = 0.1
        choice_mock.side_effect = MockRandom(0).choice
        self.player.values[get_board_state_tuple("---|-XO|---")] = 0.501
        self.assert_get_move_is(5, Board.O, "---|-X-|---")
        choice_mock.assert_called_once_with([5])

    @patch('td_learning_player.random.choice')
    @patch('td_learning_player.random.random')
    def test_get_move_chooses_random_best_available_move_if_random_gte_epsilon_and_multiple_bests(
            self, random_mock, choice_mock):
        random_mock.return_value = 0.1
        choice_mock.side_effect = MockRandom(1).choice
        self.player.values[get_board_state_tuple("X--|-XO|---")] = 0.501
        self.player.values[get_board_state_tuple("--X|-XO|---")] = 0.501
        self.player.values[get_board_state_tuple("---|-XO|X--")] = 0.501
        self.assert_get_move_is(2, Board.X, "---|-XO|---")
        choice_mock.assert_called_once_with([0, 2, 6])
