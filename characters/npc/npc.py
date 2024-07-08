import pygame
from pathlib import Path

image_folder_path = Path.cwd() / "images"


class Npc:
    """
    A class to create a player
    """

    def __init__(self, pg_game):
        """
        Initialize the character into the starting position
        """
        self.screen = pg_game.screen
        self.settings = pg_game.settings
        self.screen_rect = pg_game.screen.get_rect()

        # Load Character sprite
        self.image = pygame.image.load(image_folder_path / "heart.png")
        self.rect = self.image.get_rect()

        # Start at the bottom of the screen
        self.rect.topright = self.screen_rect.topright

    def render(self):
        """
        Draw the character in the location
        """
        self.screen.blit(self.image, self.rect)
