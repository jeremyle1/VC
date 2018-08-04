import sys
import pygame

def check_events(players):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONUP:
            print(pygame.mouse.get_pos())
            # Pops the card up from the hand when clicked.
            players[0].check_card_clicked()

def update_screen(game, screen, players):
    screen.fill((255, 255, 255))
    # Draw hands.
    for player in players:
        player.blit_hand(screen)
    # Draw marker to indicate active player.
    game.blit_active_player(screen)
