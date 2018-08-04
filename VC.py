import sys, pygame
from source.Deck import Deck
from source.Player import Player
from source.AIPlayer import AIPlayer
from source.Game import Game
import source.GameFunctions as gf

def main():
    pygame.init()
    size = width, height = 1200, 900
    gameOver = False
    screen = pygame.display.set_mode(size)

    game = Game()
    while not gameOver:
        gf.check_events(game.players)
        gf.update_screen(game, screen, game.players)
        game.next_move()
        pygame.display.flip()

if __name__ == '__main__':
    main()
