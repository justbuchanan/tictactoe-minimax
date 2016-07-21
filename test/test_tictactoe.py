import unittest

from tictactoe import *

class TestTicTacToe(unittest.TestCase):

    def test_done(self):
        brd = Board()
        self.assertFalse(brd.done())
        self.assertEqual(SQUARE_EMPTY, brd.winner())
