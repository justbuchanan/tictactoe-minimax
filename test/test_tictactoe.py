import unittest

import numpy as np
from tictactoe import *
import minimax


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

    def test_minimax(self):
        brd = Board(np.array([
            [SQUARE_O, SQUARE_O, SQUARE_EMPTY],
            [SQUARE_X, SQUARE_EMPTY, SQUARE_EMPTY],
            [SQUARE_EMPTY, SQUARE_X, SQUARE_EMPTY],
        ]))

        # minimax should choose to block O in the above board
        mv = minimax.player(brd, SQUARE_X)
        self.assertEqual((0, 2), mv)
