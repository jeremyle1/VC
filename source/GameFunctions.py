import sys
import pygame
from source.Player import Player

def check_events(players):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONUP:
            print(pygame.mouse.get_pos())
            players[0].check_card_clicked()



def update_screen(game, screen, players):
    screen.fill((255, 255, 255))
    for player in players:
        player.blit_hand(screen)
    game.blit_active_player(screen)