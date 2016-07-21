#!/usr/bin/env python3

from enum import Enum
import numpy as np
from copy import deepcopy

## square values
SQUARE_EMPTY = ' '
SQUARE_O = 'O'
SQUARE_X = 'X'


class Board:
    def __init__(self, size=3):
        self._grid = np.full((size,size), SQUARE_EMPTY, str)
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

    def all_positions(self):
        for r in range(self.size):
            for c in range(self.size):
                yield r,c

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
        return '\n-----\n'.join(['|'.join([str(x) for x in r]) for r in self.rows()])


# class InvalidMove(RuntimeError): pass


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

        mv = p(brd, s)

        if brd[mv] != SQUARE_EMPTY:
            raise InvalidMove("Square taken: %s" % mv)
        else:
            brd[mv] = s

        print(brd)
        print()
    print('Done!')
    w = brd.winner()
    print('Winner: %s' % w)
    return w

# convert from linear index (0-8) to a row, column tuple
def index_to_rc(index):
    return (int(index / 3), index % 3)

def auto_player(brd, smbl):
    # find the first open spot
    for r in range(3):
        for c in range(3):
            if brd[r,c] == SQUARE_EMPTY:
                return (r,c)

def console_player(brd, smbl):
    res = int(input('Enter choice (0-8):'))
    return index_to_rc(res)

def minimax_player(brd, smbl):

    class Node:
        def __init__(self):
            self.children = []
            self.board = None

        def height(self):
            if len(self.children) == 0:
                return 0
            else:
                return max([n.height() for n in self.children])

    symbols = []

    def subtree_for_board(brd, cur_player):
        root = Node()
        root.board = brd

        if not brd.done():
            # add subtree for all possible moves
            next_player = SQUARE_O if cur_player == SQUARE_X else SQUARE_O
            for pos in root.board.open_positions():
                sub_board = deepcopy(brd)
                sub_board[pos] = cur_player
                root.children.append(subtree_for_board(sub_board, next_player))
        else:
            # TODO: stats?
            pass

        return root


    minimax = subtree_for_board(deepcopy(brd), smbl)

    print("minimax height: %d" % minimax.height())

    return (2,2)





if __name__ == '__main__':
    run_game(minimax_player, console_player)
