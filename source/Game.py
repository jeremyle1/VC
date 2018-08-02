from source.Deck import Deck
from source.AIPlayer import AIPlayer
from source.Player import Player
from source.Card import Card


class Game:
    def __init__(self):
        self.deck = Deck()
        self.players = []
        self.__init_players()
        # All moves of the game => (Player.position, (Cards))
        self.moves = []
        # Players that are being skipped.
        self.skipped_players = []

    def __init_players(self):
        self.players.append(Player('Jeremy', 0, self.deck))
        self.players.append(AIPlayer('Bob', 1, self.deck))
        self.players.append(AIPlayer('Lamont', 2, self.deck))
        self.players.append(AIPlayer('Kobe', 3, self.deck))

        # Player with 3 of spades has the first move.
        for player in self.players:
            if player.has_3_spades():
                self.active_player = player.position
                break

    def next_move(self):
        pass

