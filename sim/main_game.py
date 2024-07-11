import sys
import pygame
from settings.game_settings import GameSettings
from characters.player.player import Player
from characters.npc.npc import Npc
from environment.text_box import TextBox


class projectG:
    def __init__(self):
        pygame.init()
        self.settings = GameSettings()
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height)
        )
        pygame.display.set_caption("ProjectG")
        self.player = Player(self)
        self.npc = Npc(self)
        self.text_box = TextBox(self)

    def run_game(self):
        while True:
            self._check_events()
            self.player.update()
            self._check_collisions()
            if self.npc.collided:
                self.npc.collided = True
            self._update_screen()

    def _check_events(self):
        text_box = self.text_box.box_settings
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
                if event.type == pygame.KEYDOWN and self.npc.collided:
                    text_box.active = True
                    if event.key == pygame.K_RETURN:
                        self.npc.messages.append(text_box.text)
                        print(f"Message sent: {text_box.text}")
                        text_box.text = ""
                    elif event.key == pygame.K_BACKSPACE:
                        text_box.text = text_box.text[:-1]
                    else:
                        text_box.text += event.unicode

    def _check_collisions(self):
        if self.player.rect.colliderect(self.npc.rect):
            self.npc.collided = True
        else:
            self.npc.collided = False

    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        self.player.render()
        self.npc.render()
        if self.npc.collided:
            self.text_box.render(self.npc)
        pygame.display.flip()


if __name__ == "__main__":
    pG = projectG()
    pG.run_game()
