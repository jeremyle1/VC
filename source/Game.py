import pygame
from source.Deck import Deck
from source.AIPlayer import AIPlayer
from source.HumanPlayer import HumanPlayer
from source.Button import Button
import source.Rules as Rules

class Game:
    marker_color = (50, 255, 0)
    def __init__(self, screen):
        self.deck = Deck()
        self.screen = screen
        self.players = []
        # Player that played two moves ago.
        self.last_player = None
        self.active_player = None
        self.__init_players()

        # All moves of the game => (Player.position, (Cards))
        self.moves = []
        # Players that are being skipped.
        self.skipped_players = []
        self.gameOver = False
        self.playAgain = True
        # Time of the latest move.
        self.last_time = pygame.time.get_ticks()

        # Second to last move that was played.
        self.previous_move = []
        # The last move that was played.
        self.last_move = []
        # Current temporary move used to update last_move.
        self.current_move = []

        self.play_button = Button('PLAY', (100, 50), (1050, 750))
        self.skip_button = Button('SKIP', (100, 50), (1050, 825))

    def __init_players(self):
        """Creates players. Finds player with 3 of spades."""
        self.players.append(HumanPlayer('Jeremy', 0))
        self.players.append(AIPlayer('Bob', 1))
        self.players.append(AIPlayer('Lamont', 2))
        self.players.append(AIPlayer('Kobe', 3))
        for player in self.players:
            player.get_new_hand(self.deck)
            try:
                player.set_card_backs()
            except AttributeError:
                pass

        # Player with 3 of spades has the first move.
        for player in self.players:
            if player.has_3_spades():
                self.active_player = player.position
                self.last_player = player.position
                break

    def blit_active_player(self):
        """Draws a rectangle next to the hand of the current active player."""
        if self.active_player == 0:
            pygame.draw.circle(self.screen, Game.marker_color, (175, 850), 10, 10)
        elif self.active_player == 1:
            pygame.draw.circle(self.screen, Game.marker_color, (1165, 130), 10, 10)
        elif self.active_player == 2:
            pygame.draw.circle(self.screen, Game.marker_color, (275, 35), 10, 10)
        elif self.active_player == 3:
            pygame.draw.circle(self.screen, Game.marker_color, (20, 130), 10, 10)

    def blit_buttons(self):
        """Draws the play and skip buttons."""
        # TODO: Blit buttons only when possible.
        if self.active_player == 0:
            self.play_button.blit_font()
            self.skip_button.blit_font()
            self.screen.blit(self.play_button.get_button_surface(), self.play_button.get_button_rect())
            self.screen.blit(self.skip_button.get_button_surface(), self.skip_button.get_button_rect())

    def blit_move(self):
        x_center = 600
        y_center = 400
        # Difference in y between previous move and current move.
        y_offset = 32

        # First move of the game.
        if not self.previous_move and self.current_move:
            x = x_center - (len(self.current_move) - 1) * 25
            y = y_center + y_offset
            for card in self.current_move:
                card.blit_center(self.screen, (x, y))
                x = x_center + 50
            self.last_move = self.current_move
            # 1 is an arbitrary value to signify that only one move has been made.
            self.previous_move = [1]
        # There is a previous move and the current move is not a skip (empty list).
        elif self.last_move and self.current_move:
            # If a new move was played, update previous and last moves. Otherwise, blit the old moves.
            if self.last_move != self.current_move:
                self.previous_move = self.last_move
                self.last_move = self.current_move

            # On the very second move, don't blit previous move because there is none.
            if self.previous_move != [1]:
                x = x_center - (len(self.previous_move) - 1) * 25
                y = y_center
                for card in self.previous_move:
                    card.blit_center(self.screen, (x, y))
                    x += 50

            x = x_center - (len(self.last_move) - 1) * 25
            y = y_center + y_offset
            # Blit current move with a slightly higher Y value.
            for card in self.last_move:
                card.blit_center(self.screen, (x, y))
                x += 50
        # TODO handle case where current move is a skip
        # There is a previous move but the current move is a skip.
        # elif self.last_move and not self.current_move:

    def num_of_non_empty_hands(self):
        num_of_hands = 0
        for player in self.players:
            if player.hand:
                num_of_hands = num_of_hands + 1
        return num_of_hands

    def next_player(self):
        """Finds the next active player."""
        self.active_player = (self.active_player + 1) % 4
        while len(self.players[self.active_player].hand) == 0 or self.active_player in self.skipped_players:
            self.active_player = (self.active_player + 1) % 4

    def reset_skipped_players(self):
        """Checks if skipped players list should be reset, and does so if necessary."""
        # Number of non-empty hands minus one.
        max_skipped = self.num_of_non_empty_hands() - 1

        # All but active player has skipped, and he plays a hand that cannot beat the previous hand, OR active player
        # runs out of cards, OR every player has skipped and the active player is the first to re-start.
        if (len(self.skipped_players) == max_skipped and not
                Rules.beats(self.last_move, self.current_move)) or (len(self.players[self.active_player].hand) == 0)\
                or (len(self.skipped_players) > max_skipped):
            self.skipped_players = []

    def next_move(self):
        temp_move = self.players[self.active_player].make_move(self, self.last_time)

