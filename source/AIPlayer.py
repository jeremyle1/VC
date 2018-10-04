import pygame
import os, random
from source.Player import Player
import source.Rules as Rules
from source.MCTS.GameState import GameState
from source.MCTS.UCT import UCT


class AIPlayer(Player):
    def __init__(self, name, position):
        Player.__init__(self, name, position)
        self.card_backs = []

    def blit_hand(self, screen):
        """Draw hand with back of card instead of front"""
        # Player on right.
        if self.position == 1:
            x = 1125
            y = 150
        # Player on top.
        elif self.position == 2:
            x = 300
            y = -125
        # Player on left.
        elif self.position == 3:
            x = -150
            y = 150

        for card in range(len(self.hand)):
            screen.blit(self.card_backs[card], (x, y))
            # Fan cards so they don't stack on top of each other.
            if self.position == 1 or self.position == 3:
                y += 35
            elif self.position == 2:
                x += 35

    def set_card_backs(self):
        """Transform and rotate back of cards"""
        for i in range(len(self.hand)):
            self.card_backs.append(pygame.image.load(os.path.join('./source/', 'images', 'card_back.png')))
        for i in range(len(self.card_backs)):
            self.card_backs[i] = pygame.transform.scale(self.card_backs[i], (150, 218))
            if self.position == 1:
                self.card_backs[i] = pygame.transform.rotate(self.card_backs[i], 270)
            elif self.position == 2:
                self.card_backs[i] = pygame.transform.rotate(self.card_backs[i], 180)
            elif self.position == 3:
                self.card_backs[i] = pygame.transform.rotate(self.card_backs[i], 90)

    def find_best_move(self, game):
        """Returns a list of cards that should be the best move to take. Returns empty list to skip turn."""
        rootstate = GameState(game.last_move, game.players, game.skipped_players, game.last_player, game.active_player)
        m = UCT(rootstate=rootstate, itermax=3)
        return m

    def make_move(self, game, last_time):
        """Process the player's turn."""
        # Pause for a short period of time before making the move.
        if pygame.time.get_ticks() - last_time > self.thinking_time:

            move = self.find_best_move(game)

            # Move is empty. Skip this player.
            if not move:
                game.last_time = pygame.time.get_ticks()
                game.skipped_players.append(self.position)
                # If no player can beat the current hand.
                if len(game.skipped_players) > game.num_of_non_empty_hands() - 1:
                    game.active_player = (game.active_player + 1) % 4
                    while len(game.players[game.active_player].hand) == 0:
                        game.active_player = (game.active_player + 1) % 4
                else:
                    game.next_player()
                return move

            game.moves.append(move)
            # Cards played during this turn are no longer in the hand.
            for card in move:
                self.hand.remove(card)

            game.current_move = move

            # Game ends after three players have empty hands.
            empty_hands = 0
            for player in game.players:
                if len(player.hand) == 0:
                    empty_hands += 1
            if empty_hands >= 3:
                game.gameOver = True
                return

            # Update time for the next player.
            game.last_time = pygame.time.get_ticks()


            # Checks if skipped players list should be reset, and does so if necessary.
            game.reset_skipped_players()
            # This player just made the last move.
            game.last_player = self.position
            # Finds next player turn.
            game.next_player()

            return move
