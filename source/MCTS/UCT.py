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

def UCT(rootstate, itermax):
    """ Conduct a UCT search for itermax iterations starting from rootstate.
            Return the best move from the rootstate."""

    rootnode = Node(state = rootstate)

    for i in range(itermax):
        print('iteration', i)
        node = rootnode
        state = rootstate.clone()

        # Select
        while node.untried_moves == [] and node.child_nodes != []: # node is fully expanded and non-terminal
            print('Select')
            node = node.UCT_select_child()
            state.do_move(node.move)

        # Expand
        if node.untried_moves != []: # if we can expand (i.e. state/node is non-terminal)
            print('Expand')
            m = random.choice(node.untried_moves)
            state.do_move(m)
            node = node.add_child(m,state) # add child and descend tree

        # Rollout - this can often be made orders of magnitude quicker using a state.GetRandomMove() function
        while (0 not in [len(player.hand) for player in state.players]): # while state is non-terminal
            # print('Rollout', state.get_moves())
            state.do_move(random.choice(state.get_moves()))

        # Backpropagate
        while node != None: # backpropagate from the expanded node and work back to the root node
            print('Backpropogate')
            if not node.parent:
                node.visits = node.visits + 1
            else:
                node.update(state.get_results(node.parent.state.active_player)) # state is terminal. Update node with result from POV of node.playerJustMoved
            node = node.parent

    return sorted(rootnode.child_nodes, key=lambda c: c.visits)[-1].move  # return the move that was most visited