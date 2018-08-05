import pygame

class Button:
    def __init__(self, text, size, pos):
        """
        :param text: text displayed on button
        :param size: (width, height) of button
        :param pos: (x, y) position of button
        """
        self.width, self.height = size
        self.x, self.y = pos
        # Set up button Surface and Rect
        self.surface = pygame.Surface((self.width, self.height))
        self.surface.fill((0, 255, 0))
        self.rect = self.surface.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        # Set up Font to be drawn on button's surface
        self.font = pygame.font.SysFont('Arial', 35, bold=True)
        self.font_surface = self.font.render(text, False, (0, 0, 0))
        self.font_rect = self.font_surface.get_rect(center=(self.width / 2, self.height / 2))

    def get_button_surface(self):
        """Returns Surface of the button."""
        return self.surface

    def get_button_rect(self):
        """Returns Rect of the button."""
        return self.rect

    def blit_font_on_button(self):
        """Draws text on the button."""
        self.surface.blit(self.font_surface, self.font_rect)