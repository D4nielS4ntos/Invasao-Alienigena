from random import randint

import pygame
from pygame.sprite import Sprite


class Bomba(Sprite):
    # Representa um alienígena
    def __init__(self, ai_settings, screen,  alien_number_x=0, row_number_y=0):
        super(Bomba, self).__init__()
        self.screen = screen 
        self.ai_settings = ai_settings
        # Imagem
        self.image = pygame.image.load('imagens/bomba_64x64.bmp')
        self.rect = self.image.get_rect()
        self.rect.x = self.rect.width 
        self.rect.y = self.rect.height
        # Movimento
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        self.alien_number_x = alien_number_x
        self.row_number_y = row_number_y
        self.alien_direction = 1 
        # Pontuação
        self.alien_points = ai_settings.alien_points

    def mostrar(self):
        self.screen.blit(self.image, self.rect)

    def update(self):
        # Move o alienigena
        # variation = randint(-5, 5) / 10
        self.y += self.ai_settings.alien_bomb_speed #+ variation
        self.rect.y = self.y

    def checar_lados(self):
        # Vê se o alienigena está em tocando um dos lados
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        if self.rect.left <= 0: 
            return True
