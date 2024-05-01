import os

import pygame
from pygame.sprite import Group

import funções as f
from config import Config
from classes.nave import Nave
from classes.estatisticas_de_jogo import GameStats
from classes.botão import Button
from classes.tabela_de_elementos import TabelaElementos
from classes.nave_mãe import Navemae


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
    table_of_elements = TabelaElementos(ai_settings, screen, stats)
    ship = Nave(ai_settings, screen, stats) # Cria a nave
    mother_ship = Navemae(ai_settings, screen, stats)
    shots = Group() # Cria um grupo de projéteis
    alien_shots = Group() # Cria um grupo de projéteis para os alienigenas
    aliens = Group() # Cria um grupo de alienigenas
    alien_bombs = Group() # Cria um grupo de bombas
    while True:
    # Laço principal
        f.events(ai_settings, screen, ship, shots, aliens, alien_bombs, stats, table_of_elements, alien_shots, play_button)
        if stats.game_active:
            ship.update()
            aliens.update()
            alien_bombs.update()
            shots.update()
            alien_shots.update()
            mother_ship.update()
            f.shots_update(ai_settings, screen, shots, aliens, alien_bombs, ship, stats, table_of_elements, alien_shots, mother_ship)
            f.aliens_update(ai_settings, stats, screen, ship, aliens, alien_bombs, shots, table_of_elements, alien_shots, mother_ship)
        f.screen_update(ai_settings, screen, ship, shots, aliens, alien_bombs, stats, play_button, table_of_elements, alien_shots, mother_ship)
run_game() 
