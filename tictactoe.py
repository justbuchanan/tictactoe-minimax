#!/usr/bin/env python3

from enum import Enum
import numpy as np

class Square(Enum):
    EMPTY = 0
    O = 1
    X = 2


class Board:
    def __init__(self, size=3):
        self._grid = np.full((size,size), Square.EMPTY)
        self._size = size

    @property
    def size(self):
        return self._size

    def cols(self):
        for i in range(self.size):
            yield self._grid[:,i]

    def rows(self):
        for i in range(self.size):
            yield self._grid[i,:]

    def diags(self):
        ii = list(range(self.size))
        a = zip(ii, ii)
        b = zip(ii, reversed(ii))
        return [[self._grid[i] for i in a], [self._grid[i] for i in b]]

    def all_runs(self):
        return self.cols() + self.rows() + self.diags()

    # returns None to indicate game isn't over
    # returns a Square value to indicate winner if it is over
    def winner(self):
        empty_count = 0
        for run in all_runs:
            # if all elements in a run are equal, it's the winner
            p = run[0]
            if (all([r == p for r in run])):
                return p
        if (self._grid == Square.EMPTY).any():
            return None
        else:
            return Square.EMPTY

    # Returns True if game is complete
    def done(self):
        return self.winner() != None

    def __str__(self):
        return '\n'.join([' '.join(r) for r in self.rows()])


class InvalidMove(RuntimeError): pass


def run_game(player1, player2):
    brd = Board()

    players = [player1, player2]
    count = 0
    while (grid) == None:
        p = players[count % len(players)]
        count += 1

        s = [Square.O, Square.X][count % len(players)]

        mv = p(grid)
        brd._grid[mv] = s
        print('\n-----')
        print(grid)
        print('-----\n')


i = 0
def auto_player(grid):
    global i
    v = (i,i)
    i += 1
    return v

def console_player(grid):
    res = raw_input('Enter choice (0-8):')
    return int(res)


run_game(auto_player, console_player)
