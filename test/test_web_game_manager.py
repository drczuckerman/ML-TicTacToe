import unittest
from mock import patch
from web_game_manager import WebGameManager
from web_game import WebGame

class TestWebGameManager(unittest.TestCase):
    def setUp(self):
        self.manager = WebGameManager()
        
    @patch('web_game_manager.time.time')
    @patch('web_game_manager.uuid.uuid4')
    def new_game(self, uuid_mock, time_mock, game_ids, time_value):
        uuid_mock.side_effect = game_ids
        time_mock.side_effect = [time_value]
        return self.manager.new_game()

    def assert_delete_game_is(self, result, game_id, game_ids, games, time_values):
        self.assertEqual(result, self.manager.delete_game(game_id))
        self.assert_web_game_dict_is(game_ids, games, time_values)

    @patch('web_game_manager.time.time')
    def assert_refresh_game_is(
            self, time_mock, result, game_id, time_mock_values, game_ids, games, time_values):
        time_mock.side_effect = time_mock_values
        self.assertEqual(result, self.manager.refresh_game(game_id))
        self.assert_web_game_dict_is(game_ids, games, time_values)

    @patch('web_game_manager.time.time')
    def assert_expire_games_is(self, time_mock, time_mock_value, game_ids, games, time_values):
        time_mock.side_effect = [time_mock_value]
        self.manager.expire_games()
        self.assert_web_game_dict_is(game_ids, games, time_values)

    def assert_web_game_dict_is(self, game_ids, games, time_values):
        expected_web_game_dict = \
        {game_id: {"game": game, "time": time_value}
             for game_id, game, time_value in zip(game_ids, games, time_values)}
        self.assertEqual(expected_web_game_dict, self.manager.web_game_dict)
    
    def test_constructor_initializes_web_game_dict(self):
        self.assertEqual({}, self.manager.web_game_dict)

    def test_new_game_gives_game_id_and_web_game_and_stores_web_game(self):
        game_id, game = self.new_game(game_ids=["unique"], time_value=1234)
        self.assertEqual("unique", game_id)
        self.assertIsInstance(game, WebGame)
        self.assert_web_game_dict_is(game_ids=["unique"], games=[game], time_values=[1234])

    def test_new_game_retries_if_game_id_not_unique(self):
        game_id1, game1 = self.new_game(game_ids=["unique"], time_value=1234)
        game_id2, game2 = self.new_game(game_ids=["unique", "unique2"], time_value=2345)
        self.assertEqual("unique", game_id1)
        self.assertEqual("unique2", game_id2)
        self.assert_web_game_dict_is(
            game_ids=["unique", "unique2"], games=[game1, game2], time_values=[1234, 2345])

    def test_get_game_returns_none_if_game_id_not_found(self):
        game = self.manager.get_game("unique")
        self.assertIsNone(game)

    def test_get_game_returns_game_if_game_id_found(self):
        game_id1, game1 = self.new_game(game_ids=["unique"], time_value=1234)
        game_id2, game2 = self.new_game(game_ids=["unique2"], time_value=2345)
        game_id3, game3 = self.new_game(game_ids=["unique3"], time_value=3456)
        game = self.manager.get_game("unique2")
        self.assertEqual(game2, game)

    def test_delete_game_does_nothing_if_game_id_not_found(self):
        game_id1, game1 = self.new_game(game_ids=["unique"], time_value=1234)
        game_id2, game2 = self.new_game(game_ids=["unique2"], time_value=2345)
        self.assertFalse(self.manager.delete_game("unique3"))
        self.assert_delete_game_is(
            result=False, game_id="unique3",
            game_ids=["unique", "unique2"], games=[game1, game2], time_values=[1234, 2345])

    def test_delete_game_deletes_game_if_game_id_found(self):
        game_id1, game1 = self.new_game(game_ids=["unique"], time_value=1234)
        game_id2, game2 = self.new_game(game_ids=["unique2"], time_value=2345)
        self.assert_delete_game_is(
            result=True, game_id="unique",
            game_ids=["unique2"], games=[game2], time_values=[2345])

    def test_refresh_game_returns_false_if_game_id_not_found(self):
        game_id1, game1 = self.new_game(game_ids=["unique"], time_value=1234)
        game_id2, game2 = self.new_game(game_ids=["unique2"], time_value=2345)
        self.assert_refresh_game_is(
            result=False, game_id="unique3", time_mock_values=[],
            game_ids=["unique", "unique2"], games=[game1, game2], time_values=[1234, 2345])

    def test_refresh_game_returns_true_and_freshens_time_if_game_id_found(self):
        game_id1, game1 = self.new_game(game_ids=["unique"], time_value=1234)
        game_id2, game2 = self.new_game(game_ids=["unique2"], time_value=2345)
        self.assert_refresh_game_is(
            result=True, game_id="unique", time_mock_values=[3456],
            game_ids=["unique", "unique2"], games=[game1, game2], time_values=[3456, 2345])

    def test_expire_games_does_nothing_if_games_not_expired(self):
        game_id1, game1 = self.new_game(game_ids=["unique"], time_value=1234)
        game_id2, game2 = self.new_game(game_ids=["unique2"], time_value=1235)
        self.assert_expire_games_is(
            time_mock_value=1234+WebGameManager.EXPIRE_TIME-1,
            game_ids=["unique", "unique2"], games=[game1, game2], time_values=[1234, 1235])

    def test_expire_games_deletes_expired_games(self):
        game_id1, game1 = self.new_game(game_ids=["unique"], time_value=1235)
        game_id2, game2 = self.new_game(game_ids=["unique2"], time_value=1234)
        game_id3, game3 = self.new_game(game_ids=["unique3"], time_value=1236)
        self.assert_expire_games_is(
            time_mock_value=1234+WebGameManager.EXPIRE_TIME,
            game_ids=["unique", "unique3"], games=[game1, game3], time_values=[1235, 1236])
