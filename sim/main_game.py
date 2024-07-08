import sys
import pygame
from settings.game_settings import GameSettings
from settings.input_box import InputBox
from characters.player.player import Player
from characters.npc.npc import Npc


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
        self.font = pygame.font.Font(None, 32)
        self.input_box = pygame.Rect(100, 100, 140, 32)
        self.text = "need to be able to update"

    def run_game(self):
        while True:
            self._check_events()
            self.player.update()
            self._check_collisions()
            if self.collided:
                self.type_box.active = True
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
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and self.collided:
                    self.type_box.active = True
                elif event.key == pygame.K_RETURN and self.type_box.active:
                    self.npc.messages.append(self.text)
                    print(f"Message sent: {self.text}")
                    self.text = ""
                    self.type_box.active = False
                elif self.type_box.active:
                    if event.key == pygame.K_BACKSPACE:
                        self.text = self.text[:-1]
                    else:
                        self.text += event.unicode

    def _check_collisions(self):
        if self.player.rect.colliderect(self.npc.rect):
            self.collided = True
        else:
            self.collided = False
            self.type_box.active = False

    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        self.player.render()
        self.npc.render()
        if self.type_box.active:
            pygame.draw.rect(self.screen, (255, 255, 255), self.input_box)
            txt_surface = self.font.render(self.text, True, (0, 0, 0))
            self.screen.blit(txt_surface, (self.input_box.x+5, self.input_box.y+5))
            self.input_box.w = max(200, txt_surface.get_width()+10)
            self._render_typebox()
        pygame.display.flip()

    def _render_typebox(self):
        y_offset = 50
        for message in self.npc.messages:
            message_surface = self.font.render(message, True, (0, 0, 0))
            self.screen.blit(message_surface, (self.input_box.x, self.input_box.y - y_offset))
            y_offset += 30
        pygame.draw.rect(self.screen, (255, 255, 255), self.input_box)
        txt_surface = self.font.render(self.text, True, (0, 0, 0))
        self.screen.blit(txt_surface, (self.input_box.x + 5, self.input_box.y + 5))
        self.input_box.w = max(200, txt_surface.get_width() + 10)


if __name__ == "__main__":
    pG = projectG()
    pG.run_game()
