import pygame.font


class Button():
# Cria um botão de play
    def __init__(self, ai_settings, screen, msg):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.width, self.height = 200, 50
        # Dimenções e propriedades do botão
        self.button_color = None
        self.text_color = ai_settings.text_color
        self.font = pygame.font.SysFont(None, 48)
        # Constroi o botão
        self.background = pygame.image.load('imagens/espaço de texto-2.png') # pygame.Rect(0, 0, self.width, self.height)
        self.background = pygame.transform.scale(self.background, (32*4, 32*4))
        self.rect = self.background.get_rect()

        self.background_positionx = self.screen_rect.centerx - self.rect.centerx
        self.background_positiony = self.screen_rect.centery - self.rect.centery
        self.rect.centerx = self.screen_rect.centerx
        self.rect.centery = self.screen_rect.centery
        self.prep_msg(msg)

    def prep_msg(self, msg):
        self.msg_image = self.font.render(msg, True, self.text_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.screen_rect.center
    
    def drawn_button(self):
        self.screen.blit(self.background, (self.background_positionx, self.background_positiony))
        self.screen.blit(self.msg_image, self.msg_image_rect)
