import unittest

from tictactoe import *

class TestTicTacToe(unittest.TestCase):

    def test(self):
        brd = Board()
        self.assertFalse(brd.done())
