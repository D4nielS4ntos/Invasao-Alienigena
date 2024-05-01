# from random import randint

import pygame
from pygame.sprite import Sprite


class Alienigena(Sprite):
    # Representa um alienígena
    def __init__(self, ai_settings, screen,  alien_number_x=0, row_number_y=0):
        super(Alienigena, self).__init__()
        self.screen = screen 
        self.ai_settings = ai_settings
        # Imagem
        self.current_image_index = 0
        self.image = pygame.image.load(f'imagens/Alienigena_32x32/sprite_{int(self.current_image_index)}.bmp')
        self.image = pygame.transform.scale(self.image, (32*2, 32*2))
        self.rect = self.image.get_rect()
        self.rect.x = self.rect.width 
        self.rect.y = self.rect.height
        # Movimento
        self.x = float(self.rect.x)
        self.alien_number_x = alien_number_x
        self.row_number_y = row_number_y
        self.alien_direction = 1 
        # Pontuação
        self.alien_points = ai_settings.alien_points
        
    def show(self):
        self.screen.blit(self.image, self.rect)

    def update(self):
        # Move o alienigena
        # if randint(1, 5) == 5:
        #     self.current_image_index += 0.1
        # if self.current_image_index > 2:
        #     self.current_image_index = 0
        # else:
        #     self.image = pygame.image.load(f'imagens/Alienigena_32x32/sprite_{int(self.current_image_index)}.bmp')

        if self.row_number_y % 2 == 0:
            self.x += (self.ai_settings.alien_speed_factor * self.alien_direction)
        if self.row_number_y % 2 == 1:
            self.x -= (self.ai_settings.alien_speed_factor * self.alien_direction)
        self.rect.x = self.x

    def check_sides(self):
        # Vê se o alienigena está em tocando um dos lados
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        if self.rect.left <= 0: 
            return True
