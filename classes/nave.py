from random import randint

import pygame
from pygame.sprite import Sprite


class Nave(Sprite):
# Cria uma nave
    def __init__(self, ai_settings, screen, stats):
    # Define a posição da nave na tela
        super(Nave, self).__init__()
        self.ai_settings = ai_settings
        self.screen = screen
        self.stats = stats
        # Imagem
        self.atual = 0
        self.image = pygame.image.load(f'imagens/Nave_32x32/sprite_0{int(self.atual)}.png')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        # Movimento
        self.center = float(self.rect.centerx)
        self.moving_right = False
        self.moving_left = False 
        self.ultima_vida()

    def mostrar(self):
    # Mostra a nave na tela
        self.screen.blit(self.image, self.rect)

    def update(self):
    # Atualiza a posição da nave
        if randint(1, 5) == 5:
            self.atual += 0.1
        if self.atual > 15:
            self.atual = 0
        elif self.atual >= 10:
            self.image = pygame.image.load(f'imagens/Nave_32x32/sprite_{int(self.atual)}.png')
        else:
            self.image = pygame.image.load(f'imagens/Nave_32x32/sprite_0{int(self.atual)}.png')
        
        if self.moving_right and self.rect.right < self.screen_rect.right: 
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0: 
            self.center -= self.ai_settings.ship_speed_factor
        self.rect.centerx = self.center

    def centrar_nave(self):
        self.center = self.screen_rect.centerx

    def ultima_vida(self):
        if self.stats.ships_left == 1:
            self.ai_settings.bullet_speed_factor *= 2 
            self.ai_settings.bullet_width *= 2
            self.ai_settings.bullet_height *= 2
            self.ai_settings.bullet_color = (255, 0, 0)
            
            som_powerup = pygame.mixer.music
            som_powerup.load('music/powerUp.wav')
            som_powerup.play()
