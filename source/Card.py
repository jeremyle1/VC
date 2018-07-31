import pygame
import os

class Card:
    ranks = [str(n) for n in range(3, 11)] + list('JQKA2')
    suits = ['spades', 'clubs', 'diamonds', 'hearts']
    def __init__(self, rank, suit):
        self.rank = str(rank)
        self.suit = str(suit)
        if self.rank not in self.ranks or self.suit not in self.suits:
            raise ValueError
        self.selected = False
        self.image = pygame.image.load(os.path.join('../', 'images', self.rank.lower() + '_' + self.suit + '.png'))
        self.scale_card()
        self.rect = self.image.get_rect()

    def hearts_high(self):
        """
        Return the positional ranking of a Card.

        Used for key arg of sort() and sorted() functions
        """
        return 4 * Card.ranks.index(self.rank) + Card.suits.index(self.suit)

    def blit_on_hand(self, screen, x, y):
        """
        Draw card on player's hand (cards that the player hasn't played yet)
        :param screen:
        :param x: x position of card
        :param y: y position of card
        """
        self.rect.x = x
        self.rect.y = y
        screen.blit(self.image, self.rect)

    def scale_card(self):
        self.image = pygame.transform.scale(self.image, (150, 218))

    """If self.selected is false, set it to true. If true, set it to false."""
    def toggle_selected(self):
        self.selected = not self.selected

    """Returns true if card is selected."""
    def is_selected(self):
        return self.selected

    def __repr__(self):
        return f'Card({self.rank}, {self.suit})'

    def __str__(self):
        return f'{self.rank} {self.suit}'
