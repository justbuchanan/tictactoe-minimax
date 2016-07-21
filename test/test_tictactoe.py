import unittest

import numpy as np
from tictactoe import *

class TestTicTacToe(unittest.TestCase):

    def test_done(self):
        brd = Board()
        self.assertFalse(brd.done())
        self.assertEqual(SQUARE_EMPTY, brd.winner())

    def test_winner(self):
        brd = Board(np.array([
                [SQUARE_O, SQUARE_X, SQUARE_O],
                [SQUARE_X, SQUARE_O, SQUARE_X],
                [SQUARE_O, SQUARE_X, SQUARE_EMPTY],
            ]))
        self.assertEqual(SQUARE_O, brd.winner())
