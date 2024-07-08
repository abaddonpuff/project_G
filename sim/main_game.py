import sys
import pygame
from settings.game_settings import GameSettings
from settings.input_box import InputBox
from characters.player.player import Player
from characters.npc.npc import Npc

INPUTBOX_DISPLAY = False

class projectG:
    def __init__(self):
        pygame.init()
        self.settings = GameSettings()
        self.input_box_settings = InputBox()
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height)
        )
        pygame.display.set_caption("ProjectG")
        self.player = Player(self)
        self.type_box = InputBox()
        self.npc = Npc(self)
        self.collided = False

    def run_game(self):
        while True:
            self._check_events()
            self.player.update()
            self._check_collisions()
            if self.type_box.active:
                self._render_typebox()
            self._update_screen()

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
            elif event.type == pygame.K_SPACE:
                self.type_box.active = True

    def _check_collisions(self):
        if self.player.rect.colliderect(self.npc.rect):
            self.collided = True
        else:
            self.collided = False

    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        self.player.render()
        self.npc.render()
        pygame.display.flip()
        print(f"collided: {self.collided}")

    def _render_typebox(self):
        self.font = pygame.font.Font(None, 32)
        self.input_box = pygame.Rect(100, 100, 140, 32)
        self.text = ""
        pygame.display.flip()

if __name__ == "__main__":
    pG = projectG()
    pG.run_game()

