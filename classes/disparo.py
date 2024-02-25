import pygame
from pygame.sprite import Sprite
from random import randint


class Disparo(Sprite):
# Cria e atualiza os disparos
    def __init__(self, ai_settings, screen, nave):
        super(Disparo, self).__init__()
        self.screen = screen
        # Posição
        self.rect = pygame.Rect(0, 0, ai_settings.bullet_width, ai_settings.bullet_height)
        self.rect.centerx = nave.rect.centerx 
        self.rect.top = nave.rect.top
        self.y = float(self.rect.y)
        # Cor
        self.color = ai_settings.bullet_color
        # Velocidade
        self.speed_factor = ai_settings.bullet_speed_factor

    def update(self):
    # Move o disparo
        self.y -= self.speed_factor
        self.rect.y = self.y
    
    def desenhar_disparo(self):
    # Desenha o disparo na tela
        pygame.draw.rect(self.screen, self.color, self.rect)


class Disparo_alienigena(Disparo):
    def __init__(self, ai_settings, screen, nave):
        super().__init__(ai_settings, screen, nave)
        self.screen = screen
        # Posição
        self.rect = pygame.Rect(0, 0, ai_settings.alien_bullet_width, ai_settings.alien_bullet_height)
        self.screen_rect = screen.get_rect()
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        # Cor
        self.color = ai_settings.alien_bullet_color
        # Velocidade
        self.speed_factor = ai_settings.alien_bullet_speed_factor
    
    def update(self):
    # Move o disparo
        self.y += self.speed_factor
        self.rect.y = self.y

    def posicao_disparo(self, alienigenas, alien_number_x, row_number_y):
    # teste
        disparo_x = randint(0, alien_number_x-1)
        disparo_y = randint(0, row_number_y-1)
        for alienigena in alienigenas.sprites():
            if disparo_x == alienigena.alien_number_x and disparo_y == alienigena.row_number_y:
                self.x = alienigena.rect.centerx
                self.y = alienigena.rect.centery
                self.rect.y = self.y
                self.rect.x = self.x
                self.rect.bottom = alienigena.rect.bottom
    
    def desenhar_disparo(self):
    # Desenha o disparo na tela
        pygame.draw.rect(self.screen, self.color, self.rect)
