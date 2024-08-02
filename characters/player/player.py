import pygame
from pathlib import Path

image_folder_path = Path.cwd() / "images"


class Player:
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
        self.image = pygame.image.load(image_folder_path / "boy.png")
        self.rect = self.image.get_rect()

        # Player starts in the same position everytime
        coord_x = 350
        coord_y = 134
        self.rect.center = (coord_x, coord_y)

        # Positional values for the character
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        # Movement flag
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

    def update(self):
        """
        Update position based on the movement flag
        """

        # Condition to avoid going out of the screen
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.char_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.char_speed
        if self.moving_up and self.rect.top > 0:
            self.y -= self.settings.char_speed
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.settings.char_speed

        self.rect.x = self.x
        self.rect.y = self.y

    def render(self):
        """
        Draw the character in the location
        """
        self.screen.blit(self.image, self.rect)
