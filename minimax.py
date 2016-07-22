from copy import deepcopy
import graphviz as gv
from tictactoe import *


class Node:
    """
    Node in minimax tree
    """

    def __init__(self):
        self.children = []
        self.board = None
        # if True, @children represents the result of each of our possible moves
        self.our_turn = None
        self.value = 0
        self.move = None  # The (r, c) position that was last taken

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
        color = 'red' if self.our_turn else 'blue'
        root = g.node(node_name,
                      label=str(self.board),
                      shape='rect',
                      color=color)

        for index, child in enumerate(self.children):
            child_name = node_name + str(index)
            child._as_graphviz(g, child_name)
            g.edge(node_name, child_name, label=str(child.move))

    # returns a graphviz.Digraph object
    def as_graphviz(self):
        g = gv.Digraph(self.__class__.__name__, format='png')
        self._as_graphviz(g, '0')
        return g


## Build a minimax tree for tictactoe board
# @param brd The current board
# @param player The player the minimax tree is for
# @param cur_player who's turn it currently is
def minimax_tree_for_board(brd, player, cur_player):
    root = Node()
    root.board = brd
    root.our_turn = (cur_player == player)

    if not brd.done():
        # add subtree for all possible moves
        next_player = other_player(cur_player)
        for pos in root.board.open_positions():
            sub_board = deepcopy(brd)
            sub_board[pos] = cur_player
            child = minimax_tree_for_board(sub_board, player, next_player)
            child.move = pos
            root.children.append(child)

        # update node's value based on child nodes
        if root.our_turn:
            root.value = max([c.value for c in root.children])
        else:
            # discount factor to prefer loss later rather than now
            root.value = min([c.value for c in root.children]) * 0.9

    else:
        # game complete, set node value based on who won
        w = brd.winner()
        if w == player:
            # we won!
            root.value = 1
        elif w == other_player(player):
            # they won :()
            root.value = -1

    return root


## A player that makes its moves using minimax
def player(brd, smbl):
    print('Thinking...')

    # build minimax tree
    minimax = minimax_tree_for_board(deepcopy(brd), smbl, smbl)

    # optional debug info
    if False:
        print('Tree height: %d' % minimax.height())
        if minimax.height() <= 5:
            print('writing minimax diagram...')
            minimax.write_diagram_png('minimax')

    # make choice based on minimax tree
    best_choice = max(list(minimax.children), key=lambda n: n.value)
    return best_choice.move
