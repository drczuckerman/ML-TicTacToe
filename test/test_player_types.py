import unittest
import player_types
from td_learning_player import TDLearningPlayer
from td_symmetric_learning_player import TDSymmetricLearningPlayer
from random_player import RandomPlayer
from human_player import HumanPlayer

class TestPlayerTypes(unittest.TestCase):
    def test_get_learning_player_for_learning_players(self):
        self.assertIsInstance(player_types.get_learning_player("TD"), TDLearningPlayer)

    def test_get_learning_player_for_non_learning_player(self):
        self.assertRaises(KeyError, player_types.get_learning_player, "Random")
        self.assertRaises(KeyError, player_types.get_learning_player, "Human")

    def test_get_learning_player_for_bad_player(self):
        self.assertRaises(KeyError, player_types.get_learning_player, "Bad")

    def test_get_player_for_learning_players(self):
        self.assertIsInstance(player_types.get_player("TD"), TDLearningPlayer)
        self.assertIsInstance(player_types.get_player("TDS"), TDSymmetricLearningPlayer)

    def test_get_player_for_non_learning_players(self):
        self.assertIsInstance(player_types.get_player("Random"), RandomPlayer)
        self.assertIsInstance(player_types.get_player("Human"), HumanPlayer)

    def test_get_player_for_bad_player(self):
        self.assertRaises(KeyError, player_types.get_player, "Bad")

    def test_get_learning_player_types(self):
        self.assertEqual(["TD", "TDS"], player_types.get_learning_player_types())

    def test_get_player_types(self):
        self.assertEqual(["Human", "Random", "TD", "TDS"], player_types.get_player_types())

    def test_get_learning_player_descriptions(self):
        self.assertEqual(
            ["Temporal Difference Learning Player", "Temporal Difference Symmetric Learning Player"],
            player_types.get_learning_player_descriptions())

    def test_get_player_descriptions(self):
        self.assertEqual(
            [
                "Human Player",
                "Random Player",
                "Temporal Difference Learning Player",
                "Temporal Difference Symmetric Learning Player"
            ], player_types.get_player_descriptions())

    def test_get_learning_player_command_line_args(self):
        self.assertEqual(
            "- TD: Temporal Difference Learning Player\n"
            "- TDS: Temporal Difference Symmetric Learning Player",
            player_types.get_learning_player_command_line_args())
