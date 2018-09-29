import pygame
from source.Player import Player
import source.Rules as Rules

class HumanPlayer(Player):
    def __init__(self, name, position, deck):
        Player.__init__(self, name, position, deck)

    def blit_hand(self, screen):
        """Draw all cards of the player's hand."""
        if self.position == 0:
            x = 200
            y = 800
            y_offset = 50
            for card in self.hand:
                # Card is selected and should be higher than the rest of the hand.
                if card.is_selected():
                    card.blit_on_hand(screen, x, y - y_offset)
                else:
                    card.blit_on_hand(screen, x, y)
                # Fan cards so they don't stack on top of each other.
                x += 50

    def check_card_clicked(self):
        """Checks if mouse position overlaps with a card's rect and toggles the card accordingly."""
        clicked_card = -1
        for card in self.hand:
            if card.rect.collidepoint(pygame.mouse.get_pos()):
                # Last card that mouse position collides with.
                clicked_card = self.hand.index(card)

        if clicked_card >= 0:
            self.hand[clicked_card].toggle_selected()

    def skip_btn_clicked(self, game):
        if game.skip_button.hovered() and game.active_player == 0 and game.last_player != self.position:
            game.last_time = pygame.time.get_ticks()
            game.skipped_players.append(self.position)
            # No player can beat the current hand.
            if len(game.skipped_players) > game.num_of_non_empty_hands() - 1:
                game.active_player = (game.active_player + 1) % 4
                while len(game.players[game.active_player].hand) == 0:
                    game.active_player = (game.active_player + 1) % 4
            else:
                game.next_player()

    def play_btn_clicked(self, game):
        # Mouse should be over the play button at the time of click.
        # Active player should be human. Move should be valid.
        if game.play_button.hovered() and game.active_player == 0 and self.validate_move(game):
            move = self.get_selected_cards()
            game.moves.append(move)
            for card in move:
                self.hand.remove(card)

        # Game ends after three players have empty hands.
            empty_hands = 0
            for player in game.players:
                if len(player.hand) == 0:
                    empty_hands += 1
            if empty_hands == 3:
                game.gameOver = True
                return

            game.last_time = pygame.time.get_ticks()

            if move:
                game.current_move = move

            # Checks if skipped players list should be reset, and does so if necessary.
            game.reset_skipped_players()
            # This player just made the last move.
            game.last_player = self.position
            # Find next player turn.
            game.next_player()

    def validate_move(self, game):
        """Returns True if the selected cards can beat the current hand."""
        cards = self.get_selected_cards()
        max_skipped = game.num_of_non_empty_hands() - 1
        # Return True if selected cards can beat the last move, False otherwise.
        if game.last_move and len(game.skipped_players) < max_skipped:
            return Rules.beats(game.last_move, self.get_selected_cards())
        # Other players have skipped their turns, so any valid move can now be played.
        elif game.last_move and len(game.skipped_players) == max_skipped and game.last_player == self.position:
            return (len(cards) == 1 or Rules.double(cards) or Rules.triple(cards) or Rules.quad(cards) or
                    Rules.straight(cards) or Rules.double_straight(cards))
        # No player can beat the current hand. Next move can be anything.
        elif len(game.skipped_players) > max_skipped:
            return (len(cards) == 1 or Rules.double(cards) or Rules.triple(cards) or Rules.quad(cards) or
                    Rules.straight(cards) or Rules.double_straight(cards))
        # First move of the game. Return True if the selected cards make up a valid move.
        else:
            return (len(cards) == 1 or Rules.double(cards) or Rules.triple(cards) or Rules.quad(cards) or
                    Rules.straight(cards) or Rules.double_straight(cards)) and\
                   (cards[0].rank == '3' and cards[0].suit == 'spades')

    def get_selected_cards(self):
        """"Returns a list of the selected cards."""
        cards = [card for card in self.hand if card.selected]
        return cards

    def make_move(self, game, last_time):
        pass