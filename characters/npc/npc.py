import pygame
from pathlib import Path

image_folder_path = Path.cwd() / "images"

class Npc:
    def __init__(self, pg_game):
        self.screen = pg_game.screen
        self.settings = pg_game.settings
        self.screen_rect = pg_game.screen.get_rect()
        self.image = pygame.image.load(image_folder_path / "heart.png")
        self.rect = self.image.get_rect()
        self.rect.topright = self.screen_rect.topright
        self.messages = []

    def render(self):
        self.screen.blit(self.image, self.rect)
