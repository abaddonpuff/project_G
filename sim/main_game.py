import sys
import pygame
from settings.settings import Settings
from characters.player.player import Player

class projectG:
    '''
    Class to manage game assets and behavior
    '''

    def __init__(self):
        '''
        Initialize game and create game resources
        '''
        pygame.init()

        self.settings = Settings()

        self.screen = pygame.display.set_mode((self.settings.screen_width,
                                                self.settings.screen_height))
        pygame.display.set_caption("ProjectG")
        self.player = Player(self)


    def run_game(self):
        '''
        Start the main loop of the game
        '''
        while True:
            #Watch for keyboard and mouse events.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            #Make screen visible
            self.screen.fill(self.settings.bg_color)
            self.player.render()
            pygame.display.flip()

if __name__ == '__main__':
    pG = projectG()
    pG.run_game()