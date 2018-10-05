# Written by Peter Cowling, Ed Powley, Daniel Whitehouse (University of York, UK) September 2012.
#
# Licence is granted to freely use and distribute for any sensible/legal purpose so long as this comment
# remains in any distributed code.
#
# For more information about Monte Carlo Tree Search check out our web site at www.mcts.ai
#
# Modifications made by Jeremy Le.

from source.MCTS.Node import Node
import random
from pygame import time

def UCT(rootstate, itermax):
    """ Conduct a UCT search for itermax iterations starting from rootstate.
            Return the best move from the rootstate."""

    rootnode = Node(state = rootstate)
    start_time = time.get_ticks()
    # Time in milliseconds the algorithm should run for.
    thinking = 4500
    # Number of iterations.
    iter = 0

    # Algorithm stops running when total time the algorithm has run exceeds thinking time, or iter becomes
    # greater than itermax
    while(time.get_ticks() - start_time < thinking) and (iter < itermax):
        iter = iter + 1
        # print('iteration', iter)
        node = rootnode
        state = rootstate.clone()

        # Select
        while node.untried_moves == [] and node.child_nodes != []: # node is fully expanded and non-terminal
            node = node.UCT_select_child()
            state.do_move(node.move)

        # Expand
        if node.untried_moves != []: # if we can expand (i.e. state/node is non-terminal)
            m = random.choice(node.untried_moves)
            state.do_move(m)
            node = node.add_child(m,state) # add child and descend tree

        # Rollout - this can often be made orders of magnitude quicker using a state.GetRandomMove() function
        while (0 not in [len(player.hand) for player in state.players]): # while state is non-terminal
            state.do_move(random.choice(state.get_moves()))

        # Backpropagate
        while node != None: # backpropagate from the expanded node and work back to the root node
            if not node.parent:
                node.visits = node.visits + 1
            else:
                node.update(state.get_results(node.parent.state.active_player)) # state is terminal. Update node with result from POV of node.playerJustMoved
            node = node.parent

    return sorted(rootnode.child_nodes, key=lambda c: c.visits)[-1].move  # return the move that was most visited