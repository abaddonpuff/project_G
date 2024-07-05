import sys
import pygame
from settings.settings import Settings
from characters.player.player import Player


class projectG:
    """
    Class to manage game assets and behavior
    """

    def __init__(self):
        """
        Initialize game and create game resources
        """
        pygame.init()

        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height)
        )
        pygame.display.set_caption("ProjectG")
        self.player = Player(self)

    def run_game(self):
        """
        Start the main loop of the game
        """
        while True:
            # Watch for keyboard and mouse events.
            self._check_events()
            # Check Player movements
            self.player.update()

            # Make screen visible
            self._update_screen()

    def _check_events(self):
        """
        Responds to keypresses and mouse events
        """

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.player.moving_right = True
                elif event.key == pygame.K_LEFT:
                    self.player.moving_left = True
                elif event.key == pygame.K_UP:
                    self.player.moving_up = True
                elif event.key == pygame.K_DOWN:
                    self.player.moving_down = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    self.player.moving_right = False
                elif event.key == pygame.K_LEFT:
                    self.player.moving_left = False
                elif event.key == pygame.K_UP:
                    self.player.moving_up = False
                elif event.key == pygame.K_DOWN:
                    self.player.moving_down = False

    def _update_screen(self):
        """
        Update images on the screen and go to the next screen
        """
        self.screen.fill(self.settings.bg_color)
        self.player.render()

        pygame.display.flip()


if __name__ == "__main__":
    pG = projectG()
    pG.run_game()
