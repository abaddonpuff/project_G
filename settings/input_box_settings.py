import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)


class InputBoxSettings:
    """
    A class to store InputBox Settings
    """

    def __init__(self, pg_game):
        """
        Initialize input box's settings
        """
        self.screen_rect = pg_game.screen.get_rect()
        self.color_inactive = GRAY
        self.color_active = BLACK
        self.color = self.color_inactive
        self.active = False
        self.collided = False
        self.font = pygame.font.Font(None, 32)
        self.box_rect = pygame.Rect(
            0,
            self.screen_rect.height - self.screen_rect.height * 0.20,
            self.screen_rect.width,
            self.screen_rect.height * 0.20,
        )
        # self.box_rect = pygame.Rect(100, 100, 140, 32)
        # self.screen_rect.height

        # TODO place text box relative to the character?
        self.y_offset = 50
        self.text = ""

    def settings(self):
        """
        Initialize input box's settings
        """
        pass
