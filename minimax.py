from copy import deepcopy
import graphviz as gv
from tictactoe import *


# returns a ((row, col), player) indicating who and where a move was made
# returns None if brdBefore == brdAfter
def find_move(brdBefore, brdAfter):
    for r in range(brdBefore.size):
        for c in range(brdBefore.size):
            if brdBefore[r, c] != brdAfter[r, c]:
                return (r, c), brdAfter[r, c]
    return None


class Node:
    def __init__(self):
        self.children = []
        self.board = None
        # if True, @children represents the result of each of our possible moves
        self.our_turn = None
        self.value = 0
        self.parent = None

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
            move, player = find_move(root.board, child.board)
            g.edge(node_name, child_name, label='%s: %s' % (player, str(pos)))

    # returns a graphviz.Digraph object
    def as_graphviz(self):
        g = gv.Digraph(self.__class__.__name__, format='png')
        self._as_graphviz(g, '0')
        return g

    def __hash__(self):
        return hash(self.board) ^ hash(self.our_turn)

    def __eq__(self, other):
        return self.board == other.board and self.our_turn == other.our_turn


_minimax_cache = {}


## Build a minimax tree for tictactoe board
# @param brd The current board
# @param player The player the minimax tree is for
# @param cur_player who's turn it currently is
def minimax_tree_for_board(brd, player, cur_player):
    use_cache = True

    root = Node()
    root.board = brd
    root.our_turn = (cur_player == player)

    # retrieve from cache
    if use_cache:
        if root in _minimax_cache:
            # print('cache hit!')
            return _minimax_cache[root]

    if not brd.done():

        def create_subtree(pos):
            sub_board = deepcopy(brd)
            sub_board[pos] = cur_player
            child = minimax_tree_for_board(sub_board, player, next_player)
            return child

        # add subtree for all possible moves
        next_player = other_player(cur_player)
        root.children = [create_subtree(pos)
                         for pos in root.board.open_positions()]

        # update parent pointer for all child nodes
        for c in root.children:
            c.parent = root

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

    if use_cache:
        _minimax_cache[root] = root

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
    pos, player = find_move(minimax.board, best_choice.board)
    return pos
