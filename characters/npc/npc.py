import json
import pygame
from pathlib import Path
from environment.text_box import TextBox

image_folder_path = Path.cwd() / "images"
settings_folder_path = Path.cwd() / "characters" / "npc" / "npc_settings.json"


class Npc:
    def __init__(self, pg_game, npc_key=1):
        settings_path = str(settings_folder_path)
        settings_file = open(settings_path, "r")
        npc_dict = json.load(settings_file)
        keys_list = list(npc_dict.keys())
        key = keys_list[npc_key]
        self.personality = npc_dict[key]["attributes"]
        self.image = pygame.image.load(npc_dict[key]["settings"]["image_path"])
        self.screen = pg_game.screen
        self.settings = pg_game.settings
        self.screen_rect = pg_game.screen.get_rect()
        self.rect = self.image.get_rect()
        coord_x = npc_dict[key]["settings"]["coordinates"][0]
        coord_y = npc_dict[key]["settings"]["coordinates"][1]
        self.rect.topleft = (coord_x, coord_y)

        self.collided = False
        self.text_box = TextBox(pg_game)
        self.messages = []

    def render(self):
        self.screen.blit(self.image, self.rect)

    def render_messages(self):
        self.text_box.render(self.messages)
