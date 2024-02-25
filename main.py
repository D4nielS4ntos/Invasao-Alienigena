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
    tabelapontos = TabelaPontos(ai_settings, screen, stats)
    nave = Nave(ai_settings, screen, stats) # Cria a nave
    disparos = Group() # Cria um grupo de projéteis
    disparos_alienigenas = Group() # Cria um grupo de projéteis para os alienigenas
    alienigenas = Group() # Cria um grupo de alienigenas
    while True:
    # Laço principal
        # stats.cronometro()
        f.checar_eventos(ai_settings, screen, nave, disparos, alienigenas, stats, tabelapontos, disparos_alienigenas, play_button)
        if stats.game_active:
            nave.update()
            alienigenas.update()
            disparos.update()
            disparos_alienigenas.update() 
            f.atualizar_disparos(ai_settings, screen, disparos, alienigenas, nave, stats, tabelapontos, disparos_alienigenas)
            f.atualizar_alienigenas(ai_settings, stats, screen, nave, alienigenas, disparos, tabelapontos, disparos_alienigenas)
        f.atualizar_tela(ai_settings, screen, nave, disparos, alienigenas, stats, play_button, tabelapontos, disparos_alienigenas)
run_game()
