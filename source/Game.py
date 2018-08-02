import pygame
from source.Deck import Deck
from source.AIPlayer import AIPlayer
from source.Player import Player
from source.Card import Card


class Game:
    marker_color = (50, 255, 0)
    def __init__(self):
        self.deck = Deck()
        self.players = []
        self.__init_players()
        # All moves of the game => (Player.position, (Cards))
        self.moves = []
        # Players that are being skipped.
        self.skipped_players = []

    def __init_players(self):
        """Creates players. Finds player with 3 of spades."""
        self.players.append(Player('Jeremy', 0, self.deck))
        self.players.append(AIPlayer('Bob', 1, self.deck))
        self.players.append(AIPlayer('Lamont', 2, self.deck))
        self.players.append(AIPlayer('Kobe', 3, self.deck))

        # Player with 3 of spades has the first move.
        for player in self.players:
            if player.has_3_spades():
                self.active_player = player.position
                break

    def blit_active_player(self, screen):
        """Draws a rectangle next to the hand of the current active player."""
        if self.active_player == 0:
            pygame.draw.rect(screen, Game.marker_color, (175, 850, 20, 20))
        elif self.active_player == 1:
            pygame.draw.rect(screen, Game.marker_color, (1165, 130, 20, 20))
        elif self.active_player == 2:
            pygame.draw.rect(screen, Game.marker_color, (275, 35, 20, 20))
        elif self.active_player == 3:
            pygame.draw.rect(screen, Game.marker_color, (20, 130, 20, 20))

    def next_move(self):
        pass
