#!/usr/bin/env python3

from enum import Enum
import numpy as np

## square values
SQUARE_EMPTY = 0
SQUARE_O = 1
SQUARE_X = 2


class Board:
    def __init__(self, size=3):
        self._grid = np.full((size,size), SQUARE_EMPTY, int)
        self._size = size

    @property
    def size(self):
        return self._size

    def cols(self):
        return [self._grid[:,i] for i in range(self.size)]

    def rows(self):
        return [self._grid[i,:] for i in range(self.size)]

    def diags(self):
        ii = list(range(self.size))
        a = zip(ii, ii)
        b = zip(ii, reversed(ii))
        return [[self._grid[i] for i in a], [self._grid[i] for i in b]]

    def all_runs(self):
        return self.cols() + self.rows() + self.diags()

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
        return '\n'.join([' '.join([str(x) for x in r]) for r in self.rows()])


# class InvalidMove(RuntimeError): pass


# first player is O, second is X
# each player is a function that returns an (r, c) tuple
def run_game(player1, player2):
    brd = Board()

    players = [player1, player2]
    count = 0
    while not brd.done():
        p = players[count % len(players)]
        count += 1

        # symbol for current player
        s = [SQUARE_O, SQUARE_X][count % len(players)]

        mv = p(brd)

        if brd[mv] != SQUARE_EMPTY:
            raise InvalidMove("Square taken: %s" % mv)
        else:
            brd[mv] = s

        print('\n-----')
        print(brd)
        print('-----\n')
    print('Done!')

def index_to_rc(index):
    return (int(index / 3), index % 3)

def auto_player(brd):
    # find the first open spot
    for r in range(3):
        for c in range(3):
            if brd[r,c] == SQUARE_EMPTY:
                return (r,c)

def console_player(grid):
    res = int(input('Enter choice (0-8):'))
    return index_to_rc(res)


if __name__ == '__main__':
    run_game(auto_player, console_player)
