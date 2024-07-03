import pygame
import os

image_folder_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '..', 'images')
class Player:
    '''
    A class to create a player
    '''

    def __init__(self, pg_game):
        '''
        Initialize the character into the starting position
        '''
        self.screen = pg_game.screen
        self.screen_rect = pg_game.screen.get_rect()

        #Load Character sprite
        self.image = pygame.image.load(image_folder_path+'/turtle.bmp')
        self.rect = self.image.get_rect()

        #Start at the bottom of the screen
        self.rect.midbottom = self.screen_rect.midbottom

    def render(self):
        '''
        Draw the character in the location
        '''
        self.screen.blit(self.image, self.rect)