import pygame
from pygame.sprite import Sprite
from random import randint


class Disparo(Sprite):
# Cria e atualiza os disparos
    def __init__(self, ai_settings, screen, ship):
        super(Disparo, self).__init__()
        # self.ai_settings = ai_settings
        self.screen = screen
        # self.ship = ship
        # Posição
        self.rect_image = pygame.image.load('imagens/Disparo_2.png').convert()
        self.rect = self.rect_image.get_rect()
        # self.rect_image = pygame.transform.scale(self.rect_image, (16*1, 16*1))
        # self.rect_x = self.rect_image.get_width()
        # self.rect_y = self.rect_image.get_height()
        # self.rect = pygame.Rect(0, 0, ai_settings.bullet_width, ai_settings.bullet_height)
        # self.background_positionx = self.screen_rect.centerx - self.rect.centerx
        # self.background_positiony = self.screen_rect.centery - self.rect.centery
        self.rect.centerx = ship.rect.centerx 
        self.rect.top = ship.rect.top
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        # Cor
        self.color = ai_settings.bullet_color
        # Velocidade
        self.speed_factor = ai_settings.bullet_speed_factor
        # Vidas da nave
        self.last_life = False

    def update(self):
    # Move o disparo
        self.y -= self.speed_factor
        self.rect.y = self.y
    
    def drawn_shot(self, ship):
    # Desenha o disparo na tela
        # pygame.draw.rect(self.screen, self.color, self.rect)
        if ship.stats.ships_left == 1 and self.last_life == False:
            self.rect_image = pygame.transform.scale(self.rect_image, (16*2, 16*2))
            self.rect.centerx = ship.rect.centerx - self.rect.width / 2
            self.last_life = True
        self.screen.blit(self.rect_image, self.rect)


class Disparo_alienigena(Disparo):
    def __init__(self, ai_settings, screen, ship):
        super().__init__(ai_settings, screen, ship)
        self.screen = screen
        # Posição
        self.rect_image = pygame.image.load('imagens/Disparo_alienigena_2.png')
        self.rect = self.rect_image.get_rect() #pygame.Rect(0, 0, ai_settings.alien_bullet_width, ai_settings.alien_bullet_height)
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

    def shot_position(self, aliens, alien_number_x, row_number_y):
    # teste
        shot_x = randint(0, alien_number_x-1)
        shot_y = randint(0, row_number_y-1)
        for alien in aliens.sprites():
            if shot_x == alien.alien_number_x and shot_y == alien.row_number_y:
                self.x = alien.rect.centerx
                self.y = alien.rect.centery
                self.rect.y = self.y
                self.rect.x = self.x
                self.rect.bottom = alien.rect.bottom
    
    def drawn_shot(self):
    # Desenha o disparo na tela
        # pygame.draw.rect(self.screen, self.color, self.rect)
        self.screen.blit(self.rect_image, self.rect)
