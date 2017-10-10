import sys
sys.path.append("../../")

import unittest

from my_package.foo.bar import dumb_true

class TestBar(unittest.TestCase):
    def test_bar_true(self):
        self.assertTrue(dumb_true())


if __name__ == "__main__":
    unittest.main()
