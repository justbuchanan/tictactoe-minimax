#!/usr/bin/env python3

from enum import Enum
from copy import deepcopy
import numpy as np
import operator
from functools import reduce

## square values
SQUARE_EMPTY = ' '
SQUARE_O = 'O'
SQUARE_X = 'X'


def other_player(sq):
    return SQUARE_O if sq == SQUARE_X else SQUARE_X


def empty_square_matrix(size=3):
    return np.full((size, size), SQUARE_EMPTY, str)


## A tictactoe board
# By default it's a 3x3 grid, but it can be any size square.
# Positions are specified by (row, column) tuples.
class Board:
    def __init__(self, grid=empty_square_matrix(3)):
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

    ## returns SQUARE_EMPTY to indicate game isn't over
    # returns None for tie game
    # returns SQUARE_X or SQUARE_O value to indicate winner if it is over
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

    ## Returns a string of the form:
    # O| |
    # -----
    # X|O|X
    # -----
    #  | |
    def __str__(self):
        row_divider = '\n' + '-' * (self.size * 2 - 1) + '\n'
        return row_divider.join(['|'.join([str(x) for x in r])
                                 for r in self.rows()])

    def __eq__(self, other):
        return np.array_equal(self._grid, other._grid)

    def __hash__(self):
        s = reduce(operator.add, self._grid.flatten())
        return hash(s)


## Exception raised by run_game() when a player requests an invalid move
class InvalidMove(RuntimeError):
    pass


## Run a game a game of tictactoe, given two players
# first player is O, second is X
# each player is a function that returns an (r, c) tuple
def run_game(player1, player2, board_size=3):
    brd = Board(empty_square_matrix(board_size))

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
            raise InvalidMove("Square taken: %s" % str(mv))
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
    for r in range(brd.size):
        for c in range(brd.size):
            if brd[r, c] == SQUARE_EMPTY:
                return (r, c)


def console_player(brd, smbl):
    # convert from linear index (0-8) to a row, column tuple
    def index_to_rc(index):
        return (int(index / brd.size), index % brd.size)

    res = int(input('Your move (0-8):'))
    return index_to_rc(res)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description="Tic tac toe!")
    parser.add_argument("--mefirst",
                        action='store_true',
                        help="Request to go first")
    parser.add_argument("--size", default=3, type=int, help="Size of board")
    args = parser.parse_args()

    import minimax

    if args.mefirst:
        run_game(console_player, minimax.player, args.size)
    else:
        run_game(minimax.player, console_player, args.size)
