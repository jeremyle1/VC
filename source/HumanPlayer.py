import pygame
from source.Player import Player

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
            # print('Mouse position:', pygame.mouse.get_pos())
            # print('Rect Position:', card.rect)
            if card.rect.collidepoint(pygame.mouse.get_pos()):
                # Last card that mouse position collides with.
                clicked_card = self.hand.index(card)

        if clicked_card >= 0:
            self.hand[clicked_card].toggle_selected()

    def make_move(self, game, last_time):
        if pygame.time.get_ticks() - last_time > self.thinking_time:
            move = [self.hand[0]]
            game.moves.append(move)
            for card in move:
                self.hand.remove(card)
            game.last_time = pygame.time.get_ticks()
            game.active_player = (game.active_player + 1) % 4