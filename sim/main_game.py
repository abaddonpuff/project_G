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

CHARACTER_IMAGES = [
    "npc1.png",
    "npc2.png",
    "npc3.png",
    "npc4.png",
    "npc5.png",
    "npc6.png",
    "npc7.png",
]

CHARACTER_NAMES = [
    "npc1",
    "npc2",
    "npc3",
    "npc4",
    "npc5",
    "npc6",
    "npc7",
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
    (960, 178),
    (816, 299),
    (1066, 300),
    (995, 723),
    (805, 564),
    (471, 370),
    (102, 511),
    (251, 590),
    (504, 723),
]

PICKED_COORDINATES = []
PICKED_NAMES = []
PICKED_IMAGES = []


def generateNPC():
    global PICKED_COORDINATES
    global PICKED_NAMES
    global PICKED_IMAGES

    attribute_dict = defaultdict(int)
    npc_settings = defaultdict(str)
    coordinates = _pick_random_unique(COORDINATES, PICKED_COORDINATES)
    npc_name = _pick_random_unique(CHARACTER_NAMES, PICKED_NAMES)
    npc_image = _pick_random_unique(CHARACTER_IMAGES, PICKED_IMAGES)
    # while True:
    #     coordinates = random.choice(COORDINATES)
    #     if coordinates not in PICKED_COORDINATES:
    #         PICKED_COORDINATES.append(coordinates)
    #         break
    # while True:
    #     npc_name = random.choice(CHARACTER_NAMES)
    #     if npc_name not in PICKED_NAMES:
    #         PICKED_NAMES.append(npc_name)
    #         break
    # while True:
    #     npc_image = random.choice(CHARACTER_IMAGES)
    #     if npc_image not in PICKED_IMAGES:
    #         PICKED_IMAGES.append(npc_image)
    #         break

    npc_settings["name"] = npc_name
    npc_settings["image_path"] = str(image_folder_path / npc_image)
    npc_settings["coordinates"] = coordinates

    for attribute in ATTRIBUTES:
        attribute_dict[attribute] = random.randint(0, 70)

    return {npc_name: {"settings": npc_settings, "attributes": attribute_dict}}


def _pick_random_unique(global_list, global_picked_list):
    while True:
        pick = random.choice(global_list)
        if pick not in global_picked_list:
            global_picked_list.append(pick)
            break
    return pick


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
        # Load the background image
        self.background_image = pygame.image.load(str(image_folder_path / "town.png"))
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
        self.screen.blit(self.background_image, (0, 0))
        self.player.render()

        for npc, collided in self.npcs_collided.items():
            npc.render()
            if collided:
                npc.render_messages()

        pygame.display.flip()


if __name__ == "__main__":
    pG = projectG()
    pG.run_game()
