import unittest
import os
import utils

class TestUtils(unittest.TestCase):
    def test_get_path(self):
        self.assertEqual(os.path.abspath("./dir/file"), utils.get_path("dir", "file"))
