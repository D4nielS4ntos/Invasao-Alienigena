import os

import pygame
from pygame.sprite import Group

import funções as f
from config import Config
from classes.nave import Nave
from classes.estatisticas_de_jogo import GameStats
from classes.botão import Button
from classes.tabela_de_pontos import TabelaPontos


def run_game():
# Cria a tela
    os.system('cls')
    pygame.init()
    ai_settings = Config()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Invasão Alienígena")
    # pygame.display.toggle_fullscreen() # liberar quando o projeto estiver pronto
    play_button = Button(ai_settings, screen, "Play")
    stats = GameStats(ai_settings) # Armazena dados estísticos do jogo
    table_of_points = TabelaPontos(ai_settings, screen, stats)
    ship = Nave(ai_settings, screen, stats) # Cria a nave
    shots = Group() # Cria um grupo de projéteis
    alien_shots = Group() # Cria um grupo de projéteis para os alienigenas
    aliens = Group() # Cria um grupo de alienigenas
    while True:
    # Laço principal
        f.events(ai_settings, screen, ship, shots, aliens, stats, table_of_points, alien_shots, play_button)
        if stats.game_active:
            ship.update()
            aliens.update()
            shots.update()
            alien_shots.update() 
            f.shots_update(ai_settings, screen, shots, aliens, ship, stats, table_of_points, alien_shots)
            f.aliens_update(ai_settings, stats, screen, ship, aliens, shots, table_of_points, alien_shots)
        f.screen_update(ai_settings, screen, ship, shots, aliens, stats, play_button, table_of_points, alien_shots)
run_game() 
       