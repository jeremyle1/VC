# Written by Peter Cowling, Ed Powley, Daniel Whitehouse (University of York, UK) September 2012.
#
# Licence is granted to freely use and distribute for any sensible/legal purpose so long as this comment
# remains in any distributed code.
#
# For more information about Monte Carlo Tree Search check out our web site at www.mcts.ai
#
# Modifications made by Jeremy Le.

import source.Rules as Rules
from source.Card import Card
from source.Player import Player
from datetime import datetime

class GameState():
    def __init__(self, move, players, skipped, player_just_moved, active_player):
        # Current move to beat.
        self.move = move
        self.players = [player for player in players if player.hand]
        # List of currently skipped players.
        self.skipped = skipped
        # Player that played the last move (not skipped).
        self.player_just_moved = player_just_moved
        # Current player to make a move.
        self.active_player = active_player

    def clone(self):
        """Returns a deep clone of this game state.
        """
        # Create copies of each player's hand and position.
        new_players = []
        new_hands = []
        new_positions = []
        for player in self.players:
            new_hand = []
            new_positions.append(player.position)
            for card in player.hand:
                new_hand.append(Card(card.rank, card.suit, False))
            new_hands.append(new_hand)

        # Create copies of players.
        for i in range(len(self.players)):
            player_copy = Player('', new_positions[i])
            player_copy.hand = new_hands[i]
            new_players.append(player_copy)

        st = GameState(self.move[:], new_players, self.skipped[:], self.player_just_moved, self.active_player)
        return st

    def get_moves(self):
        """Returns the possible moves from this game state.
        """
        active_hand = self.players[self.get_player_index(self.active_player)].hand
        # First move of game.
        if not self.move:
            return Rules.combos_3_of_spades(active_hand)
        # Everyone has skipped. Play anything.
        elif len(self.skipped) == len(self.players):
            return Rules.all_move_combinations(active_hand)
        # Everyone but active player has skipped.
        elif (len(self.skipped) == len(self.players)-1) and self.active_player == self.player_just_moved:
            return Rules.all_move_combinations(active_hand)
        # Currently being skipped.
        elif self.active_player in self.skipped:
            return [[]]
        # Beat the last move.
        else:
            return Rules.possible_moves(self.move, active_hand)

    def do_move(self, move):
        """Updates current game state by making move."""
        # Skip turn.
        if move == [] or move == [[]]:
            if self.active_player not in self.skipped:
                self.skipped.append(self.active_player)
        else:
            # Update hand of active player.
            for card in move:
                self.players[self.get_player_index(self.active_player)].hand.remove(card)
            # Update skipped players.
            if len(self.skipped) == len(self.players)-1 and self.active_player == self.player_just_moved\
                    and not Rules.beats(self.move, move):
                self.skipped = []
            elif len(self.skipped) == len(self.players):
                self.skipped = []

            self.player_just_moved = self.active_player
            self.move = move

        # Get index of next active player.
        next_index = (self.get_player_index(self.active_player) + 1) % len(self.players)
        # Get player position using index and update the next active player.
        self.active_player = self.players[next_index].position

    def get_results(self, playerjm):
        if self.players[self.get_player_index(playerjm)].hand:
            return 0.0
        else:
            return 1.0

    def get_player_index(self, position):
        """Returns the index of the player that has the specified position.
        """
        for i in range(len(self.players)):
            if self.players[i].position == position:
                return i

    def last_player_in_players(self):
        """Returns True if the player that made the last move is still in self.players, False otherwise."""
        for player in self.players:
            if player.position == self.player_just_moved:
                return True
        return False
