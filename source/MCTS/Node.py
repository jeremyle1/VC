class Node():
    def __init__(self, move=None, parent=None, state=None):
        self.move = move
        self.parent = parent
        self.state = state
        self.child_nodes = []
        self.untried_moves = state.get_moves()
        self.player_just_moved = state.player_just_moved
        self.wins = 0
        self.visits = 0