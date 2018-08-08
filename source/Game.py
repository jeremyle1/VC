import pygame
from source.Deck import Deck
from source.AIPlayer import AIPlayer
from source.HumanPlayer import HumanPlayer
from source.Button import Button

class Game:
    marker_color = (50, 255, 0)
    def __init__(self, screen):
        self.deck = Deck()
        self.screen = screen
        self.players = []
        self.__init_players()
        # All moves of the game => (Player.position, (Cards))
        self.moves = []
        # Players that are being skipped.
        self.skipped_players = {i : (False, []) for i in range(4)}
        self.gameOver = False
        self.playAgain = True
        self.last_time = pygame.time.get_ticks()

        self.previous_move = []
        self.last_move = []
        self.current_move = []

        self.play_button = Button('PLAY', (100, 50), (1050, 750))
        self.skip_button = Button('SKIP', (100, 50), (1050, 825))

    def __init_players(self):
        """Creates players. Finds player with 3 of spades."""
        self.players.append(HumanPlayer('Jeremy', 0, self.deck))
        self.players.append(AIPlayer('Bob', 1, self.deck))
        self.players.append(AIPlayer('Lamont', 2, self.deck))
        self.players.append(AIPlayer('Kobe', 3, self.deck))

        # Player with 3 of spades has the first move.
        for player in self.players:
            if player.has_3_spades():
                self.active_player = player.position
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





    def next_move(self):
        if self.active_player == 0:
            # Check if player is skipped by comparing their skipped move to the current move.
            # Check when play button or skip button is clicked.
            # If skip button pressed:
                # Increment active_player
                # Add (player position, type of move) to self.skipped_players
            # If move valid:
                # Add move to self.moves. Remove card from player's hand.
            # Increment self.active_player
            pass
        else:
            pass
            # Check if player is skipped by comparing their skipped move to the current move.
            # Find best move for AI.
            # Wait 5 seconds.
            # Make move
            # If player skips, Add (player position, type of move) to self.skipped_players
            # Else:
                # # Add move to self.moves. Remove card from player's hand.
            # Increment self.active_player
        temp_move = self.players[self.active_player].make_move(self, self.last_time)
        if temp_move is not None:
            self.current_move = temp_move

        # First move of game.
        # if not self.previous_move and self.current_move:
        #     # Blit move in center.
        #     self.blit_move(self.current_move, 600, 450)
        # elif previous_move and current_move:
        #     # Blit last move with higher Y.
        #     # Blit current move in center.
        #     #previous_move = last_move
        #     #last_move = current_move
        # elif previous_move and not current_move:
        #     # Blit previous move with higher Y.
        #     # Blit last move in center.

