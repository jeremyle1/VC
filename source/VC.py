import sys, pygame
from Deck import Deck
from Player import Player
from AIPlayer import AIPlayer
import GameFunctions as gf

def main():
    pygame.init()
    size = width, height = 1200, 900
    gameOver = False
    screen = pygame.display.set_mode(size)

    deck = Deck()

    players = []
    players.append(Player('Jeremy', 0, deck))
    players.append(AIPlayer('Bob', 1, deck))
    players.append(AIPlayer('Lamont', 2, deck))
    players.append(AIPlayer('Kobe', 3, deck))

    while not gameOver:
        gf.check_events(players)
        gf.update_screen(screen, players)
        pygame.display.flip()

if __name__ == '__main__':
    main()