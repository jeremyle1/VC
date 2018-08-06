import sys, pygame
from source.Game import Game
import source.GameFunctions as gf

def main():
    pygame.init()
    size = width, height = 1200, 900
    screen = pygame.display.set_mode(size)

    playAgain = True
    while playAgain:
        game = Game(screen)
        while not game.gameOver:
            gf.check_events(game)
            game.next_move()
            gf.update_screen(game, screen, game.players)
            pygame.display.flip()
        # Ask if player wants to play again.
        playAgain = game.playAgain

if __name__ == '__main__':
    main()
