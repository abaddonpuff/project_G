import pygame
from settings.input_box_settings import InputBoxSettings


class TextBox:
    """
    A class to startup a textbox
    """

    def __init__(self, pg_game):
        """
        Initialize the textbox into the position and assign settings
        """
        self.screen = pg_game.screen
        self.box_settings = InputBoxSettings(pg_game)
        self.screen_rect = pg_game.screen.get_rect()

    def render(self, npc):
        """
        Draw the Text in the right place
        """
        text_box_rect = self.box_settings.box_rect
        y_offset = 50
        for message in npc.messages:
            message_surface = self.box_settings.font.render(message, True, (0, 0, 0))
            self.screen.blit(
                message_surface, (text_box_rect.x, text_box_rect.y - y_offset)
            )
            y_offset += 30
        pygame.draw.rect(self.screen, (255, 255, 255), text_box_rect)
        txt_surface = self.box_settings.font.render(
            self.box_settings.text, True, (0, 0, 0)
        )
        self.screen.blit(txt_surface, (text_box_rect.x + 5, text_box_rect.y + 5))
        # self.box_settings.box_rect.w = max(200, txt_surface.get_width() + 10)
