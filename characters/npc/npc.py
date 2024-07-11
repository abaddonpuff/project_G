from enum import Enum
from pathlib import Path

import pygame

from environment.text_box import TextBox

image_folder_path = Path.cwd() / "images"

class Position(Enum):
    TOP_LEFT = 1
    TOP_RIGHT = 2
    BOTTOM_LEFT = 3
    BOTTOM_RIGHT = 4

class Npc:
    def __init__(self, pg_game, top_offset=0, left_offset=0):
        self.screen = pg_game.screen
        self.settings = pg_game.settings
        self.screen_rect = pg_game.screen.get_rect()
        self.image = pygame.image.load(image_folder_path / "heart.png")
        #self.rect = self.image.get_rect()
        #self.rect.topright = self.screen_rect.topright
        # render on the bottom left
        self.rect = self.image.get_rect()

        # TODO: set the coords
        self.rect.bottomleft = self.screen_rect.bottomleft
        # self.rect = ...

        self.collided = False
        self.text_box = TextBox(pg_game)
        self.messages = []

    def render(self):
        self.screen.blit(self.image, self.rect)

    def render_messages(self):
        self.text_box.render(self.messages)
