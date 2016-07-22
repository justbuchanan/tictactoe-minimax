#!/usr/bin/env python3

from enum import Enum
from copy import deepcopy
import numpy as np

## square values
SQUARE_EMPTY = ' '
SQUARE_O = 'O'
SQUARE_X = 'X'


def other_player(sq):
    return SQUARE_O if sq == SQUARE_X else SQUARE_X


class Board:

    def __init__(self, grid=np.full((3, 3), SQUARE_EMPTY, str)):
        if grid.shape[0] != grid.shape[1]:
            raise RuntimeError("Grid must be a square")

        self._grid = deepcopy(grid)
        self._size = grid.shape[0]

    @property
    def size(self):
        return self._size

    def cols(self):
        return [self._grid[:, i] for i in range(self.size)]

    def rows(self):
        return [self._grid[i, :] for i in range(self.size)]

    def diags(self):
        ii = list(range(self.size))
        a = zip(ii, ii)
        b = zip(ii, reversed(ii))
        return [[self._grid[i] for i in a], [self._grid[i] for i in b]]

    def all_runs(self):
        return self.cols() + self.rows() + self.diags()

    def all_positions(self):
        for r in range(self.size):
            for c in range(self.size):
                yield r, c

    def open_positions(self):
        for pos in self.all_positions():
            if self[pos] == SQUARE_EMPTY:
                yield pos

    def __getitem__(self, index):
        return self._grid[index]

    def __setitem__(self, index, value):
        self._grid[index] = value

    # returns SQUARE_EMPTY to indicate game isn't over
    # returns None for tie game
    # returns a Square value to indicate winner if it is over
    def winner(self):
        empty_count = 0
        for run in self.all_runs():
            # if all elements in a run are equal, it's the winner
            p = run[0]
            if (all([r == p for r in run])):
                return p
        if (self._grid == SQUARE_EMPTY).any():
            # game not over yet
            return SQUARE_EMPTY
        else:
            # tie game
            return None

    # Returns True if game is complete
    def done(self):
        return self.winner() != SQUARE_EMPTY

    def __str__(self):
        return '\n-----\n'.join(['|'.join([str(x) for x in r])
                                 for r in self.rows()])


class InvalidMove(RuntimeError):

    pass


## Run a game a game of tictactoe, given two players
# first player is O, second is X
# each player is a function that returns an (r, c) tuple
def run_game(player1, player2):
    brd = Board()

    players = [player1, player2]
    symbols = [SQUARE_O, SQUARE_X]
    count = 0
    while not brd.done():
        p = players[count % len(players)]
        count += 1

        # symbol for current player
        s = symbols[count % len(players)]

        print(brd)
        print()

        mv = p(brd, s)

        if brd[mv] != SQUARE_EMPTY:
            raise InvalidMove("Square taken: %s" % mv)
        else:
            brd[mv] = s

    # print final board
    print(brd)
    print()

    # print and return result
    w = brd.winner()
    if w == None:
        print('Tie game!')
    else:
        print('Winner: %s' % w)
    return w


## Simple player that moves in the first open spot on the board
def dumb_player(brd, smbl):
    for r in range(3):
        for c in range(3):
            if brd[r, c] == SQUARE_EMPTY:
                return (r, c)


def console_player(brd, smbl):
    # convert from linear index (0-8) to a row, column tuple
    def index_to_rc(index):
        return (int(index / 3), index % 3)

    res = int(input('Your move (0-8):'))
    return index_to_rc(res)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description="Tic tac toe!")
    parser.add_argument("--mefirst",
                        action='store_true',
                        help="Request to go first")
    args = parser.parse_args()

    import minimax

    if args.mefirst:
        run_game(console_player, minimax.player)
    else:
        run_game(minimax.player, console_player)
