import pygame.font
from pygame.sprite import Group

from classes.nave import Nave


class TabelaPontos:
    def __init__(self, ai_settings, screen, stats):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings
        self.stats = stats
        # Fonte
        self.text_color = ai_settings.text_color
        self.font = pygame.font.SysFont(None, 48)
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()
        self.prep_name()

    def prep_score(self):
        rounded_score = int(round(self.stats.score, -1)) 
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True, self.text_color,
                                            None)
        # Exibe pontuação
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20
    
    def prep_high_score(self):
        high_score_name = self.stats.high_score_name
        high_score = int(round(self.stats.high_score, -1)) 
        high_score_str = "{:,} [{}]".format(high_score, high_score_name) 
        self.high_score_image = self.font.render(high_score_str, True, self.text_color, 
                                                None)

        self.high_score_rect = self.high_score_image.get_rect() 
        self.high_score_rect.centerx = self.screen_rect.centerx 
        self.high_score_rect.top = self.score_rect.top

    def prep_level(self):
        self.level_image = self.font.render(str(self.stats.level), True, self.text_color, 
                                            self.ai_settings.table_color)
        # Posiciona o nível abaixo da pontuação 
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right 
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_ships(self):
        self.ships = Group()
        for ship_number in range(self.ai_settings.ship_limit):
            ship = Nave(self.ai_settings, self.screen, self.stats)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            if ship_number < self.stats.ships_left:
                self.ships.add(ship)
            else:
                ship_explosion = Nave(self.ai_settings, self.screen, self.stats)
                ship_explosion.image = pygame.image.load('imagens/Explosão.png')
                ship_explosion.rect.x = 10 + ship_number * ship.rect.width
                ship_explosion.rect.y = 10
                self.ships.add(ship_explosion)

    def prep_name(self):
        self.name_str = "[{}]".format(self.stats.name.upper())
        self.name_format = self.font.render(self.name_str, True, self.text_color,
                                            self.ai_settings.table_color)
        self.name_str_rect = self.name_format.get_rect() 
        self.name_str_rect.x = self.screen_rect.centerx - self.name_str_rect.width / 2
        self.name_str_rect.y = 50 
        
        if self.ai_settings.writen_name == False and self.stats.name != 'digite seu nome...':
            self.stats.name = self.stats.name.removeprefix('digite seu nome...')
            self.ai_settings.writen_name = True


    def show_score(self):
        pygame.draw.rect(self.screen, self.ai_settings.table_color, (0, 0, self.ai_settings.screen_width, 50))
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        if self.stats.game_active == False:
            self.screen.blit(self.name_format, self.name_str_rect)
        self.ships.draw(self.screen)
