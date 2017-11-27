import unittest
import random
import pickle
import os
from mock import patch, Mock
from io import BytesIO
from td_learning_player import TDLearningPlayer
from learning_computer_player import run_if_learner
from computer_player import run_if_computer
from human_player import run_if_human
from board import Board
from board_test_utils import get_board_state_tuple, set_board, assert_get_move_is, \
    assert_get_move_values_are
from mock_random import MockRandom

class TestTDLearningPlayer(unittest.TestCase):
    def setUp(self):
        self.player = TDLearningPlayer()
        self.file_name_prefix = "TDLearningPlayer"
        self.board = Board()
        self.player.set_board(self.board)
        self.player.enable_learning()
        self.func = Mock()

    def assert_stored_states_are(self, pieces_list, position, piece):
        self.board.make_move(position, piece)
        self.player.store_state()
        states = list(map(get_board_state_tuple, pieces_list))
        self.assertEqual(self.player.states, states)
        
    def assert_get_reward_is(self, reward, winner, piece):
        self.player.set_piece(piece)
        self.assertAlmostEqual(reward, self.player._get_reward(winner))
        
    def assert_get_value_and_state_is(self, value, pieces, winner, piece):
        self.player.set_piece(piece)
        state = get_board_state_tuple(pieces)
        current_value, new_state = self.player._get_value_and_state(state, winner)
        self.assertAlmostEqual(value, current_value)
        self.assertEqual(state, new_state)
        self.assertIn(state, self.player.values)
        
    def assert_values_after_reward_are(self, values, pieces_list, winner):
        self.player.set_piece(Board.X)
        values_dict = {}
        for pieces, value in zip(pieces_list, values):
            set_board(self.board, pieces)
            self.player.store_state()
            values_dict[get_board_state_tuple(pieces)] = value
        self.player.set_reward(winner)
        self.assertEqual(sorted(values_dict.keys()), sorted(self.player.values.keys()))
        for key, value in self.player.values.items():
            self.assertAlmostEqual(self.player.values[key], value)

    @patch('builtins.open', create=True)
    def assert_load_values_are(self, values, piece, filename, open_mock):
        self.player.piece = None
        params = {"alpha": 0.2, "epsilon": 0.3, "x_draw_reward": 0.45, "o_draw_reward": 0.55}
        open_mock.return_value = BytesIO(pickle.dumps({"learned": values, "params": params}))
        self.player.load(piece)
        self.assertEqual(piece, self.player.piece)
        self.assertEqual(values, self.player.values)
        self.assertAlmostEqual(0.2, self.player.alpha)
        self.assertAlmostEqual(0.3, self.player.epsilon)
        self.assertAlmostEqual(0.45, self.player.draw_rewards[Board.X])
        self.assertAlmostEqual(0.55, self.player.draw_rewards[Board.O])
        self.assert_file_opened_with(filename, "rb", open_mock)

    def assert_file_opened_with(self, filename, mode, open_mock):
        open_mock.assert_called_once_with(os.path.abspath(os.path.join(".", "data", filename)), mode)
    
    @patch('pickle.dump')
    @patch('builtins.open', create=True)
    def assert_save_values_are(self, values, piece, filename, open_mock, dump_mock):
        open_mock.return_value = BytesIO()
        self.player.set_piece(piece)
        params = {"alpha": 0.05, "epsilon": 0.2, "x_draw_reward": 0.55, "o_draw_reward": 0.45}
        self.player.set_params(**params)
        self.player.values = values
        self.player.save()
        self.assert_file_opened_with(filename, "wb", open_mock)
        dump_mock.assert_called_once_with({"learned": values, "params": params}, open_mock.return_value)

    def test_constructor_initializes_board_and_piece_to_none(self):
        player = TDLearningPlayer()
        self.assertIsNone(player.piece)
        self.assertIsNone(player.board)

    def test_constructor_initializes_empty_values(self):
        self.assertEqual({}, self.player.values)
        
    def test_constructor_initializes_stored_states(self):
        self.assertEqual([], self.player.states)

    def test_constructor_disables_learning(self):
        player = TDLearningPlayer()
        self.assertFalse(player.learning)

    def test_constructor_initializes_alpha(self):
        self.assertEqual(TDLearningPlayer.DEFAULT_ALPHA, self.player.alpha)

    def test_constructor_initializes_epsilon(self):
        self.assertAlmostEqual(TDLearningPlayer.DEFAULT_EPSILON, self.player.epsilon)

    def test_constructor_initializes_draw_reward(self):
        self.assertAlmostEqual(TDLearningPlayer.DEFAULT_X_DRAW_REWARD, self.player.draw_rewards[Board.X])
        self.assertAlmostEqual(TDLearningPlayer.DEFAULT_O_DRAW_REWARD, self.player.draw_rewards[Board.O])

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
        self.player.alpha = TDLearningPlayer.DEFAULT_ALPHA+0.1
        self.player.set_params()
        self.assertAlmostEqual(TDLearningPlayer.DEFAULT_ALPHA, self.player.alpha)

    def test_set_params_sets_alpha_if_specified(self):
        self.player.set_params(alpha=TDLearningPlayer.DEFAULT_ALPHA*2)
        self.assertAlmostEqual(TDLearningPlayer.DEFAULT_ALPHA*2, self.player.alpha)

    def test_set_params_sets_default_epsilon_if_not_specified(self):
        self.player.epsilon = TDLearningPlayer.DEFAULT_EPSILON+0.05
        self.player.set_params()
        self.assertAlmostEqual(TDLearningPlayer.DEFAULT_EPSILON, self.player.epsilon)

    def test_set_params_sets_epsilon_if_specified(self):
        self.player.set_params(epsilon=TDLearningPlayer.DEFAULT_EPSILON*2)
        self.assertAlmostEqual(TDLearningPlayer.DEFAULT_EPSILON*2, self.player.epsilon)

    def test_set_params_sets_default_draw_rewards_if_not_specified(self):
        self.player.draw_rewards[Board.X] = TDLearningPlayer.DEFAULT_X_DRAW_REWARD-0.1
        self.player.draw_rewards[Board.O] = TDLearningPlayer.DEFAULT_O_DRAW_REWARD+0.1
        self.player.set_params()
        self.assertAlmostEqual(TDLearningPlayer.DEFAULT_X_DRAW_REWARD, self.player.draw_rewards[Board.X])
        self.assertAlmostEqual(TDLearningPlayer.DEFAULT_O_DRAW_REWARD, self.player.draw_rewards[Board.O])

    def test_set_params_sets_specified_x_reward_if_specified(self):
        self.player.set_params(x_draw_reward=TDLearningPlayer.DEFAULT_X_DRAW_REWARD-0.1)
        self.assertAlmostEqual(TDLearningPlayer.DEFAULT_X_DRAW_REWARD-0.1, self.player.draw_rewards[Board.X])
        self.assertAlmostEqual(TDLearningPlayer.DEFAULT_O_DRAW_REWARD, self.player.draw_rewards[Board.O])

    def test_set_params_sets_specified_o_reward_if_specified(self):
        self.player.set_params(o_draw_reward=TDLearningPlayer.DEFAULT_O_DRAW_REWARD+0.1)
        self.assertAlmostEqual(TDLearningPlayer.DEFAULT_X_DRAW_REWARD, self.player.draw_rewards[Board.X])
        self.assertAlmostEqual(TDLearningPlayer.DEFAULT_O_DRAW_REWARD+0.1, self.player.draw_rewards[Board.O])

    def test_set_params_sets_specified_x_and_o_reward_if_specified(self):
        self.player.set_params(
            x_draw_reward=TDLearningPlayer.DEFAULT_X_DRAW_REWARD-0.01, 
            o_draw_reward=TDLearningPlayer.DEFAULT_O_DRAW_REWARD+0.01)
        self.assertAlmostEqual(
            TDLearningPlayer.DEFAULT_X_DRAW_REWARD-0.01, self.player.draw_rewards[Board.X])
        self.assertAlmostEqual(
            TDLearningPlayer.DEFAULT_O_DRAW_REWARD+0.01, self.player.draw_rewards[Board.O])

    def test_get_params(self):
        params = \
        {
            "alpha": self.player.DEFAULT_ALPHA+0.01,
            "epsilon": TDLearningPlayer.DEFAULT_EPSILON-0.01,
            "x_draw_reward": TDLearningPlayer.DEFAULT_X_DRAW_REWARD+0.1,
            "o_draw_reward": TDLearningPlayer.DEFAULT_O_DRAW_REWARD-0.1
        }
        self.player.set_params(**params)
        self.assertEqual(params, self.player.get_params())

    def test_store_state_appends_state(self):
        self.assert_stored_states_are(["X--|---|---"], 0, Board.X)
        self.assert_stored_states_are(["X--|---|---", "XO-|---|---"], 1, Board.O)
        self.assert_stored_states_are(["X--|---|---", "XO-|---|---", "XOX|---|---"], 2, Board.X)
        
    def test_reset_initializes_stored_states(self):
        self.assert_stored_states_are(["---|-X-|---"], 4, Board.X)
        self.player.reset()
        self.assertEqual([], self.player.states)

    def test_disable_learning_disables_learning(self):
        self.player.disable_learning()
        self.assertFalse(self.player.learning)

    def test_enable_learning_enables_learning(self):
        self.player.enable_learning()
        self.assertTrue(self.player.learning)

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

    def test_get_value_and_state_returns_0_5_if_non_ending_state_not_stored(self):
        self.assert_get_value_and_state_is(0.5, "X--|---|---", None, Board.X)

    def test_get_value_and_state_returns_1_if_winning_state(self):
        self.assert_get_value_and_state_is(1.0, "O-O|XXX|---", Board.X, Board.X)
        self.assert_get_value_and_state_is(1.0, "OX-|O-X|OX-", Board.O, Board.O)

    def test_get_value_and_state_returns_0_if_losing_state(self):
        self.assert_get_value_and_state_is(0.0, "XOX|-O-|XO-", Board.O, Board.X)
        self.assert_get_value_and_state_is(0.0, "--X|OX-|XO-", Board.X, Board.O)

    def test_get_value_and_state_returns_draw_reward_if_draw_state(self):
        self.player.set_params(x_draw_reward=0.3, o_draw_reward=0.7)
        self.assert_get_value_and_state_is(0.3, "XXO|OOX|XOX", Board.DRAW, Board.X)
        self.assert_get_value_and_state_is(0.7, "OOX|XXO|OXO", Board.DRAW, Board.O)

    def test_get_value_and_state_returns_current_value_if_state_known(self):
        state1 = get_board_state_tuple("X--|---|---")
        state2 = get_board_state_tuple("XO-|---|---")
        self.player.values[state1] = 0.6
        self.player.values[state2] = 0.3
        self.assert_get_value_and_state_is(0.6, "X--|---|---", None, Board.X)
        self.assert_get_value_and_state_is(0.3, "XO-|---|---", None, Board.O)

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

    def test_set_reward_does_not_update_values_for_each_state_if_learning_disabled(self):
        self.player.disable_learning()
        self.player.values[get_board_state_tuple("---|-X-|---")] = 0.6
        self.player.values[get_board_state_tuple("-O-|-X-|---")] = 0.55
        self.player.values[get_board_state_tuple("-O-|-X-|--X")] = 0.7
        self.player.values[get_board_state_tuple("-OO|-X-|--X")] = 0.85
        self.player.values[get_board_state_tuple("XOO|-X-|--X")] = 1.0
        self.assert_values_after_reward_are(
            [0.6, 0.55, 0.7, 0.85, 1.0],
            ["---|-X-|---",
             "-O-|-X-|---",
             "-O-|-X-|--X",
             "-OO|-X-|--X",
             "XOO|-X-|--X"],
            Board.X)

    @patch('td_learning_player.random.choice')
    @patch('td_learning_player.random.random')
    def test_get_move_chooses_random_available_move_if_random_lt_epsilon(
            self, random_mock, choice_mock):
        random_mock.return_value = 0.099
        choice_mock.side_effect = MockRandom(4).choice
        assert_get_move_is(self, self.player, self.board, 6, Board.X, "X--|-O-|---")
        choice_mock.assert_called_once_with([1, 2, 3, 5, 6, 7, 8])

    @patch('td_learning_player.random.choice')
    @patch('td_learning_player.random.random')
    def test_get_move_chooses_best_available_move_if_random_gte_epsilon(
            self, random_mock, choice_mock):
        random_mock.return_value = 0.1
        choice_mock.side_effect = MockRandom(0).choice
        self.player.values[get_board_state_tuple("---|-XO|---")] = 0.501
        assert_get_move_is(self, self.player, self.board, 5, Board.O, "---|-X-|---")
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
        assert_get_move_is(self, self.player, self.board, 2, Board.X, "---|-XO|---")
        choice_mock.assert_called_once_with([0, 2, 6])

    @patch('td_learning_player.random.choice')
    @patch('td_learning_player.random.random')
    def test_get_move_chooses_best_available_move_if_learning_disabled(self, random_mock, choice_mock):
        self.player.disable_learning()
        random_mock.return_value = 0.099
        choice_mock.side_effect = MockRandom(0).choice
        self.player.values[get_board_state_tuple("---|-O-|--X")] = 0.501
        assert_get_move_is(self, self.player, self.board, 4, Board.O, "---|---|--X")
        random_mock.assert_not_called()
        choice_mock.assert_called_once_with([4])

    def test_get_num_states_returns_zero_initially(self):
        self.assertEqual(0, self.player.get_num_states())

    def test_get_num_states_returns_correct_num_of_states(self):
        self.player.values[get_board_state_tuple("---|-X-|---")] = 0.9
        self.player.values[get_board_state_tuple("---|-X-|--O")] = 0.75
        self.player.values[get_board_state_tuple("---|XX-|--O")] = 0.7
        self.assertEqual(3, self.player.get_num_states())

    def test_get_move_values_returns_move_values_for_available_moves(self):
        self.player.values[get_board_state_tuple("XOO|---|-X-")] = 0.7
        self.player.values[get_board_state_tuple("XO-|O--|-X-")] = 0.65
        self.player.values[get_board_state_tuple("XO-|-O-|-X-")] = 0.75
        self.player.values[get_board_state_tuple("XO-|--O|-X-")] = 0.62
        self.player.values[get_board_state_tuple("XO-|---|OX-")] = 0.72
        self.player.values[get_board_state_tuple("XO-|---|-XO")] = 0.67
        assert_get_move_values_are(
            self, self.player, self.board, {2: 0.7, 3: 0.65, 4: 0.75, 5: 0.62, 6: 0.72, 8: 0.67},
            Board.O, "XO-|---|-X-")
        
    def test_load_stores_values_for_x(self):
        values = {"foo": "bar"}
        self.assert_load_values_are(values, Board.X, self.file_name_prefix + "X.pkl")

    def test_load_stores_values_for_o(self):
        values = {"bar": "foo"}
        self.assert_load_values_are(values, Board.O, self.file_name_prefix + "O.pkl")

    def test_save_stores_values_for_x(self):
        values = {"baz": "quux"}
        self.assert_save_values_are(values, Board.X, self.file_name_prefix + "X.pkl")

    def test_save_stores_values_for_o(self):
        values = {"quux": "baz"}
        self.assert_save_values_are(values, Board.O, self.file_name_prefix + "O.pkl")

    def test_indicate_move(self):
        self.assertEqual("My move is 8", self.player.indicate_move(7))

    def test_run_if_learner_runs_function_if_td_learner(self):
        run_if_learner(self.player, self.func)
        self.func.assert_called_once_with()

    def test_run_if_computer_runs_function_if_td_learner(self):
        run_if_computer(self.player, self.func)
        self.func.assert_called_once_with()

    def test_run_if_human_does_not_run_function_if_td_learner(self):
        run_if_human(self.player, self.func)
        self.func.assert_not_called()
