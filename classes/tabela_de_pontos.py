import json
import time

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
        self.font_answer = pygame.font.SysFont(None, 36)
        self.font_first_place = pygame.font.SysFont(None, 48)
        self.font_second_place = pygame.font.SysFont(None, 36)
        self.font_third_place = pygame.font.SysFont(None, 24)
        self.font_first_place.set_underline(True)
        self.font_second_place.set_underline(True)
        self.font_third_place.set_underline(True)
        # self.font = pygame.font.SysFont(None, 48) respostas
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()
        self.prep_name()
        self.prep_menu()

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
        self.high_score_image = self.font_first_place.render(high_score_str, True, (218, 165, 32), 
                                                None)
        self.high_score_rect = self.high_score_image.get_rect() 
        self.high_score_rect.centerx = self.screen_rect.centerx 
        self.high_score_rect.bottom = self.score_rect.bottom - 5

        second_high_score_name = self.stats.second_high_score_name
        second_high_score = int(round(self.stats.second_high_score, -1)) 
        second_high_score_str = "{} [{}]".format(second_high_score, second_high_score_name) 
        self.second_high_score_image = self.font_second_place.render(second_high_score_str, True, (192, 192, 192), 
                                                None)
        self.second_high_score_rect = self.second_high_score_image.get_rect() 
        self.second_high_score_rect.x = self.high_score_rect.right + 5
        self.second_high_score_rect.bottom = self.score_rect.bottom - 5

        third_high_score_name = self.stats.third_high_score_name
        third_high_score = int(round(self.stats.third_high_score, -1)) 
        third_high_score_str = "{} [{}]".format(third_high_score, third_high_score_name) 
        self.third_high_score_image = self.font_third_place.render(third_high_score_str, True, (137, 66, 24), 
                                                None)
        self.third_high_score_rect = self.third_high_score_image.get_rect() 
        self.third_high_score_rect.x = self.second_high_score_rect.right + 5
        self.third_high_score_rect.bottom = self.score_rect.bottom - 5

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
                ship_explosion.image = pygame.image.load('imagens/explosão.png')
                ship_explosion.rect.x = 10 + ship_number * ship.rect.width
                ship_explosion.rect.y = 10
                self.ships.add(ship_explosion)

    def prep_name(self):
        self.name_str = "[{}]".format(self.stats.name.upper())
        self.name_format = self.font.render(self.name_str, True, self.text_color,
                                            self.ai_settings.table_color)
        self.name_str_rect = self.name_format.get_rect() 
        self.name_str_rect.x = self.screen_rect.centerx - self.name_str_rect.width / 2
        self.name_str_rect.y = self.ai_settings.top_rect 
        
        if self.ai_settings.writen_name == False and self.stats.name != 'digite seu nome...':
            self.stats.name = self.stats.name.removeprefix('digite seu nome...')
            self.ai_settings.writen_name = True

    def prep_question(self):
        json_questions_arquive = open('perguntas.json', encoding='utf-8')
        json_questions_table = json.load(json_questions_arquive)
        self.pergunta = json_questions_table['perguntas'][self.stats.current_question]

        question_text = "{}".format(self.pergunta['texto_pergunta'])
        self.question_format = self.font.render(question_text, True, self.text_color,
                                            self.ai_settings.table_color)
        self.question_text_rect = self.question_format.get_rect() 
        self.question_text_rect.x = self.screen_rect.centerx - self.question_text_rect.width / 2
        self.question_text_rect.y = self.ai_settings.top_rect 
    
    def prep_answers(self):
        # A
        a_letter_text = "{}".format('A) ')
        self.a_letters_format = self.font.render(a_letter_text, True, self.text_color,
                                            self.ai_settings.table_color)
        self.a_letter_text_rect = self.a_letters_format.get_rect() 
        self.a_letter_text_rect.x = 0
        self.a_letter_text_rect.y = self.screen_rect.bottom - self.a_letter_text_rect.height * 4

        a_answers_text = "{}".format(self.pergunta['resposta_A'])
        self.a_answers_format = self.font_answer.render(a_answers_text, True, self.text_color,
                                            None)
        self.a_answers_text_rect = self.a_answers_format.get_rect()
        self.a_answers_text_rect.x = self.a_answers_text_rect.height * 2
        self.a_answers_text_rect.y = self.screen_rect.bottom - self.a_answers_text_rect.height - self.a_letter_text_rect.height * 3

        # B
        b_letter_text = "{}".format('B) ')
        self.b_letters_format = self.font.render(b_letter_text, True, self.text_color,
                                            self.ai_settings.table_color)
        self.b_letter_text_rect = self.b_letters_format.get_rect() 
        self.b_letter_text_rect.x = 0
        self.b_letter_text_rect.y = self.screen_rect.bottom - self.b_letter_text_rect.height * 3

        self.b_answers_text = "{}".format(self.pergunta['resposta_B'])
        self.b_answers_format = self.font_answer.render(self.b_answers_text, True, self.text_color,
                                            None)
        self.b_answers_text_rect = self.b_answers_format.get_rect()
        self.b_answers_text_rect.x = self.b_answers_text_rect.height * 2
        self.b_answers_text_rect.y = self.screen_rect.bottom - self.b_answers_text_rect.height - self.b_letter_text_rect.height * 2

        # C
        c_letter_text = "{}".format('C) ')
        self.c_letters_format = self.font.render(c_letter_text, True, self.text_color,
                                            self.ai_settings.table_color)
        self.c_letter_text_rect = self.c_letters_format.get_rect() 
        self.c_letter_text_rect.x = 0
        self.c_letter_text_rect.y = self.screen_rect.bottom - self.c_letter_text_rect.height * 2

        self.c_answers_text = "{}".format(self.pergunta['resposta_C'])
        self.c_answers_format = self.font_answer.render(self.c_answers_text, True, self.text_color,
                                            None)
        self.c_answers_text_rect = self.c_answers_format.get_rect()
        self.c_answers_text_rect.x = self.c_answers_text_rect.height * 2
        self.c_answers_text_rect.y = self.screen_rect.bottom - self.c_answers_text_rect.height - self.c_letter_text_rect.height

        # D
        d_letter_text = "{}".format('D) ')
        self.d_letters_format = self.font.render(d_letter_text, True, self.text_color,
                                            self.ai_settings.table_color)
        self.d_letter_text_rect = self.d_letters_format.get_rect() 
        self.d_letter_text_rect.x = 0
        self.d_letter_text_rect.y = self.screen_rect.bottom - self.d_letter_text_rect.height

        self.d_answers_text = "{}".format(self.pergunta['resposta_D'])
        self.d_answers_format = self.font_answer.render(self.d_answers_text, True, self.text_color,
                                            None)
        self.d_answers_text_rect = self.d_answers_format.get_rect()
        self.d_answers_text_rect.x = self.d_answers_text_rect.height * 2
        self.d_answers_text_rect.y = self.screen_rect.bottom - self.d_answers_text_rect.height

    def prep_menu(self):
        menu_text = "{}".format('menu')
        self.menu_format = self.font.render(menu_text, True, self.text_color,
                                            self.ai_settings.table_color)
        self.menu_text_rect = self.menu_format.get_rect() 
        self.menu_text_rect.x = self.screen_rect.right - self.menu_text_rect.width
        self.menu_text_rect.y = self.screen_rect.bottom - self.menu_text_rect.height

    def prep_timer(self):
        seconds = self.stats.current_time - self.stats.initial_time
        timer_text = "{:.2f}".format(seconds)
        self.timer_format = self.font.render(timer_text, True, self.text_color,
                                            self.ai_settings.table_color)
        self.timer_text_rect = self.timer_format.get_rect() 
        self.timer_text_rect.x = self.screen_rect.right - self.timer_text_rect.width
        self.timer_text_rect.y = self.screen_rect.bottom - self.menu_text_rect.height

    def show_score(self):
        pygame.draw.rect(self.screen, self.ai_settings.table_color, (0, 0, self.ai_settings.screen_width, self.ai_settings.top_rect))
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.level_image, self.level_rect)

        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.second_high_score_image, self.second_high_score_rect)
        self.screen.blit(self.third_high_score_image, self.third_high_score_rect)

        if self.ai_settings.questions == True:
            self.screen.blit(self.question_format, self.question_text_rect)
            if self.ai_settings.time_of_question == False:
                self.stats.time_of_question_set = self.stats.current_time
                self.ai_settings.time_of_question = True
            if self.stats.current_time < self.stats.time_of_question_set + 10:
                self.screen.blit(self.a_letters_format, self.a_letter_text_rect)
                self.screen.blit(self.b_letters_format, self.b_letter_text_rect)
                self.screen.blit(self.c_letters_format, self.c_letter_text_rect)
                self.screen.blit(self.d_letters_format, self.d_letter_text_rect)
                self.screen.blit(self.a_answers_format, self.a_answers_text_rect)
                self.screen.blit(self.b_answers_format, self.b_answers_text_rect)
                self.screen.blit(self.c_answers_format, self.c_answers_text_rect)
                self.screen.blit(self.d_answers_format, self.d_answers_text_rect)

        if self.stats.game_active == True:
            self.screen.blit(self.timer_format, self.timer_text_rect)

        if self.stats.game_active == False:
            self.screen.blit(self.name_format, self.name_str_rect)
            self.screen.blit(self.menu_format, self.menu_text_rect)
        self.ships.draw(self.screen)
