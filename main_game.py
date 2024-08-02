import sys
import pygame
import random
import json
from mechanics.input_processing import generate_response
from collections import defaultdict
from settings.game_settings import GameSettings
from characters.player.player import Player
from characters.npc.npc import Npc
from pathlib import Path

image_folder_path = Path.cwd() / "images"
settings_folder_path = Path.cwd() / "characters" / "npc" / "npc_settings.json"


CHARACTER_NAMES = [
    "npc1",
    "npc2",
    "npc3",
    "npc4",
    "npc5",
    "npc6",
    "npc7",
    "npc8",
    "npc9",
    "npc10",
    "npc11",
    "npc12",
    "npc13",
    "npc14",
]
ATTRIBUTES = [
    "Intelligence",
    "Honesty",
    "Patience",
    "Humor",
    "Ambition",
    "Affection",
    "Confidence",
    "Adventurousness",
    "Empathy",
]
COORDINATES = [
    (0, 0),
    (0, 256),
    (0, 512),
    (256, 0),
    (256, 256),
    (256, 512),
    (512, 0),
    (512, 256),
    (768, 0),
    (768, 256),
    (768, 512),
]
PICKED_COORDINATES = []


def generateNPC():
    global PICKED_COORDINATES

    attribute_dict = defaultdict(int)
    npc_settings = defaultdict(str)

    npc_name = random.sample(CHARACTER_NAMES, 1)[0]
    npc_settings["name"] = npc_name
    npc_settings["image_path"] = str(image_folder_path / "heart.png")
    while True:
        coordinates = random.choice(COORDINATES)
        if coordinates not in PICKED_COORDINATES:
            PICKED_COORDINATES.append(coordinates)
            break
    npc_settings["coordinates"] = coordinates

    for attribute in ATTRIBUTES:
        attribute_dict[attribute] = random.randint(0, 99)

    return {npc_name: {"settings": npc_settings, "attributes": attribute_dict}}


def generate_npc_file(num_npc=6):
    npc_json = {}
    with open(settings_folder_path, "w") as jsonfile:
        for item in range(num_npc):
            npc_json.update(generateNPC())
        json.dump(npc_json, jsonfile, indent=4)


class projectG:
    def __init__(self, num_characters=2):
        generate_npc_file(num_npc=num_characters)
        pygame.init()
        self.settings = GameSettings()
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height)
        )
        pygame.display.set_caption("ProjectG")
        self.player = Player(self)
        # TODO: get the dimensions from the game, and then use randint in
        # self.coords to place the npcs in random locations in the grid
        # self.coords = ...
        # update npc instance below to get coords
        self.npcs = [Npc(self, x) for x in range(num_characters)]
        self.npcs_collided = {npc: False for npc in self.npcs}

    def run_game(self):
        while True:
            self._check_events()
            self.player.update()

            for npc in self.npcs:
                if self.player.rect.colliderect(npc.rect):
                    self.npcs_collided[npc] = True
                else:
                    self.npcs_collided[npc] = False

            self._update_screen()

    def _get_collided_characters(self) -> list[Npc]:
        characters = [npc for npc, collided in self.npcs_collided.items() if collided]
        if len(characters) > 1:
            raise RuntimeError("More than one character collided")
        return characters

    def _check_events(self):
        key_map = {
            pygame.K_RIGHT: "moving_right",
            pygame.K_LEFT: "moving_left",
            pygame.K_UP: "moving_up",
            pygame.K_DOWN: "moving_down",
        }

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type in (pygame.KEYDOWN, pygame.KEYUP):
                movement = event.type == pygame.KEYDOWN
                if event.key in key_map:
                    setattr(self.player, key_map[event.key], movement)
                if event.type == pygame.KEYDOWN:
                    characters = self._get_collided_characters()
                    if characters:
                        character = characters[0]
                        text_box_event = character.text_box.box_settings
                        text_box_event.active = True
                        if event.key == pygame.K_RETURN:
                            character.messages.append(text_box_event.text)
                            print(f"Message sent: {text_box_event.text}")
                            char_response = generate_response(
                                character.personality, text_box_event.text
                            )
                            print(f"Response: {char_response}")
                            character.messages.append(char_response)
                            text_box_event.text = ""
                        elif event.key == pygame.K_BACKSPACE:
                            text_box_event.text = text_box_event.text[:-1]
                        else:
                            text_box_event.text += event.unicode

    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        self.player.render()

        for npc, collided in self.npcs_collided.items():
            npc.render()
            if collided:
                npc.render_messages()

        pygame.display.flip()


if __name__ == "__main__":
    pG = projectG()
    pG.run_game()
