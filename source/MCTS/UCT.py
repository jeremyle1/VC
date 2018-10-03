from source.MCTS.GameState import GameState
from source.MCTS.Node import Node


def UCT(rootstate, itermax):
    rootnode = Node(state=rootstate)
    return None