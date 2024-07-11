import sys
import pygame
from settings.game_settings import GameSettings
from characters.player.player import Player
from characters.npc.npc import Npc


class projectG:
    def __init__(self, num_characters=2):
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
        self.npcs = [Npc(self) for _ in range(num_characters)]
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
        characters = [
            npc for npc, collided in self.npcs_collided.items()
            if collided
        ]
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
                        character.text_box.active = True
                        if event.key == pygame.K_RETURN:
                            character.messages.append(character.text_box.text)
                            print(f"Message sent: {character.text_box.text}")
                            character.text_box.text = ""
                        elif event.key == pygame.K_BACKSPACE:
                            character.text_box.text = character.text_box.text[:-1]
                        else:
                            character.text_box.text += event.unicode

    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        self.player.render()

        for npc, collided in self.npcs_collided.items():
            npc.render()
            if npc.collided:
                npc.render_messages()

        pygame.display.flip()


if __name__ == "__main__":
    pG = projectG()
    pG.run_game()
