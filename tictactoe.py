#!/usr/bin/env python3

from enum import Enum
import numpy as np

class Square(enum):
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



def print_grid(grid):
    print('-'*5)
    for row in grid:
        print('|'.join(row))
    print('-'*5)

# @param sq An (r, c) tuple
def set_square(grid, sq, smbl):
    if grid[sq[0]][sq[1]] != ' ':
        raise RuntimeError("Error: squre '%s' already claimed" % str(sq))
    grid[sq[0]][sq[1]] = smbl


def get_col(grid, c):
    return [grid[i][c] for i in range(3)]

def get_row(grid, r):
    return [grid[r][i] for i in range(3)]


def game_winner(grid):
    for c in range(3):
        


def run_game(player1, player2):
    grid = [
        [' ',' ',' '],
        [' ',' ',' '],
        [' ',' ',' ']
    ]

    players = [player1, player2]
    symbols = ['x', 'o']
    count = 0
    while game_winner(grid) == None:
        p = players[count % len(players)]
        s = symbols[count % len(players)]
        count += 1
        move = p(grid)
        set_square(grid, move, s)
        print_grid(grid)
        print()


i = 0
def player(grid):
    global i
    v = (i,i)
    i += 1
    return v


run_game(player, player)
