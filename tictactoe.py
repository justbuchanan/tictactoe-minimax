#!/usr/bin/env python3

from enum import Enum
import numpy as np
from copy import deepcopy
import graphviz as gv

## square values
SQUARE_EMPTY = ' '
SQUARE_O = 'O'
SQUARE_X = 'X'


class Board:
    def __init__(self, grid=np.full((3,3), SQUARE_EMPTY, str)):
        if grid.shape[0] != grid.shape[1]:
            raise RuntimeError("Grid must be a square")

        self._grid = deepcopy(grid)
        self._size = grid.shape[0]

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


class InvalidMove(RuntimeError): pass


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

    # print and return result
    w = brd.winner()
    if w == None:
        print('Tie game!')
    else:
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
    res = int(input('Your move (0-8):'))
    return index_to_rc(res)

def minimax_player(brd, smbl):
    print('Thinking...')

    other_smbl = SQUARE_X if smbl == SQUARE_O else SQUARE_O

    class Node:
        def __init__(self):
            self.children = []
            self.board = None
            # if True, @children represents the result of each of our possible moves
            self.our_turn = False
            self.value = 0
            self.move = None # The (r, c) position that was last taken

        def height(self):
            if len(self.children) == 0:
                return 1
            else:
                return 1 + max([n.height() for n in self.children])


        # writes a png file of the graphviz output to the specified location
        def write_diagram_png(self, filename):
            g = self.as_graphviz()
            g.render(filename=filename, cleanup=True)

        ## @param g The digraph object
        # @return node name
        def _as_graphviz(self, g, node_name=''):
            root = g.node(node_name, label=str(self.board), shape='rect')

            for index, child in enumerate(self.children):
                child_name = node_name + str(index)
                child._as_graphviz(g, child_name)
                g.edge(node_name, child_name, label=str(child.move)) # TODO: label


        # returns a graphviz.Digraph object
        def as_graphviz(self):
            g = gv.Digraph(self.__class__.__name__, format='png')
            self._as_graphviz(g, '0')
            return g


    def subtree_for_board(brd, cur_player):
        root = Node()
        root.board = brd
        root.our_turn = (cur_player == smbl) # TODO: double check

        if not brd.done():
            # add subtree for all possible moves
            next_player = SQUARE_O if cur_player == SQUARE_X else SQUARE_O
            for pos in root.board.open_positions():
                sub_board = deepcopy(brd)
                sub_board[pos] = cur_player
                child = subtree_for_board(sub_board, next_player)
                child.move = pos
                root.children.append(child)

            # update node's value based on child nodes
            if root.our_turn:
                root.value = max([c.value for c in root.children])
            else:
                root.value = min([c.value for c in root.children]) * 0.9


        else:
            # game complete, set node value based on who won
            w = brd.winner()
            if w == smbl:
                # we won!
                root.value = 1
            elif w == other_smbl:
                # they won :()
                root.value = -1

        return root


    minimax = subtree_for_board(deepcopy(brd), smbl)
    print('Tree height: %d' % minimax.height())
    if minimax.height() <= 4:
        print('writing minimax diagram...')
        minimax.write_diagram_png('minimax')



    # TODO: rm
    # values = [n.value for n in minimax.children]
    # print('values: %s' % values)

    # make choice based on minimax tree
    best_choice = max(list(minimax.children), key=lambda n: n.value)
    return best_choice.move


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(
        description="Tic tac toe!")
    parser.add_argument(
        "--mefirst",
        action='store_true',
        help=
        "Request to go first")
    args = parser.parse_args()
    if args.mefirst:
        run_game(console_player, minimax_player)
    else:
        run_game(minimax_player, console_player)
