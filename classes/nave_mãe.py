import pygame
from pygame.sprite import Sprite


class Navemae(Sprite):
# Cria uma nave
    def __init__(self, ai_settings, screen, stats):
    # Define a posição da nave na tela
        super(Navemae, self).__init__()
        self.ai_settings = ai_settings
        self.screen = screen
        self.stats = stats
        # Imagem
        self.image = pygame.image.load('imagens/alienigena2_225x225.bmp')
        self.rect_mother_ship = self.image.get_rect()
        self.question_image_A = pygame.image.load('imagens/Nave_mãe/Letra A.png')
        self.question_image_B = pygame.image.load('imagens/Nave_mãe/Letra B.png')
        self.question_image_C = pygame.image.load('imagens/Nave_mãe/Letra C.png')
        self.question_image_D = pygame.image.load('imagens/Nave_mãe/Letra D.png')
        self.screen_rect = screen.get_rect()
        self.rect_mother_ship.centerx = self.screen_rect.centerx
        self.rect_mother_ship.top = self.screen_rect.top + 100
        # Movimento
        # self.center = float(self.rect_mother_ship.centerx)
        self.direction = 1 
        self.moving_right = False
        self.moving_left = False 
        # Imagem questões
        # A
        self.qa_rect = self.question_image_A.get_rect()
        self.qa_rect.centerx = self.rect_mother_ship.centerx - self.rect_mother_ship.height*5
        self.qa_rect.bottom = self.rect_mother_ship.bottom + self.rect_mother_ship.height*2
        # B
        self.qb_rect = self.question_image_B.get_rect()
        self.qb_rect.centerx = self.rect_mother_ship.centerx - self.rect_mother_ship.height*2
        self.qb_rect.bottom = self.rect_mother_ship.bottom + self.rect_mother_ship.height*2
        # C
        self.qc_rect = self.question_image_C.get_rect()
        self.qc_rect.centerx = self.rect_mother_ship.centerx + self.rect_mother_ship.height*2
        self.qc_rect.bottom = self.rect_mother_ship.bottom + self.rect_mother_ship.height*2
        # D
        self.qd_rect = self.question_image_D.get_rect()
        self.qd_rect.centerx = self.rect_mother_ship.centerx + self.rect_mother_ship.height*5
        self.qd_rect.bottom = self.rect_mother_ship.bottom + self.rect_mother_ship.height*2

    def show(self):
    # Mostra a nave na tela
        self.screen.blit(self.image, self.rect_mother_ship)

        self.screen.blit(self.question_image_A, self.qa_rect)
        self.screen.blit(self.question_image_B, self.qb_rect)
        self.screen.blit(self.question_image_C, self.qc_rect)
        self.screen.blit(self.question_image_D, self.qd_rect)

    def center_ship(self):
        self.rect_mother_ship.centerx = self.screen_rect.centerx

    def update(self):
    # Atualiza a posição da nave
        self.rect_mother_ship.centerx += (self.ai_settings.mothership_speed_factor * self.direction)
        self.qa_rect.centerx = self.rect_mother_ship.centerx - self.rect_mother_ship.height*5
        self.qb_rect.centerx = self.rect_mother_ship.centerx - self.rect_mother_ship.height*2
        self.qc_rect.centerx = self.rect_mother_ship.centerx + self.rect_mother_ship.height*2
        self.qd_rect.centerx = self.rect_mother_ship.centerx + self.rect_mother_ship.height*5

    def check_sides(self):
        # Vê se o alienigena está em tocando um dos lados
        screen_rect = self.screen.get_rect()
        if self.rect_mother_ship.right >= screen_rect.right or self.qd_rect.right >= screen_rect.right:
            return True
        if self.rect_mother_ship.left <= 0 or self.qa_rect.left <= 0: 
            return True
