import pygame
import os
from source.Player import Player

class AIPlayer(Player):
    def __init__(self, name, position, deck):
        Player.__init__(self, name, position, deck)
        self.card_backs = []
        self.set_card_backs()

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

        for card_back in self.card_backs:
            screen.blit(card_back, (x, y))
            # Fan cards so they don't stack on top of each other.
            if self.position == 1 or self.position == 3:
                y += 35
            elif self.position == 2:
                x += 35

    def set_card_backs(self):
        """Transform and rotate back of cards"""
        for i in range(len(self.hand)):
            self.card_backs.append(pygame.image.load(os.path.join('../', 'images', 'card_back.png')))
        for i in range(len(self.card_backs)):
            self.card_backs[i] = pygame.transform.scale(self.card_backs[i], (150, 218))
            if self.position == 1:
                self.card_backs[i] = pygame.transform.rotate(self.card_backs[i], 270)
            elif self.position == 2:
                self.card_backs[i] = pygame.transform.rotate(self.card_backs[i], 180)
            elif self.position == 3:
                self.card_backs[i] = pygame.transform.rotate(self.card_backs[i], 90)


