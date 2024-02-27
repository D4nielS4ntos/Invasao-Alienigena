import sys
from time import sleep
from random import randint

import pygame

from classes.disparo import Disparo, Disparo_alienigena
from classes.alienigena import Alienigena
from classes.bomba import Bomba


def eventos_keydown(event, ai_settings, screen, stats, nave, disparos): 
# Faz parte de eventos
    if event.key == pygame.K_RIGHT: 
        nave.moving_right = True
    if event.key == pygame.K_LEFT: 
        nave.moving_left = True
    if event.key == pygame.K_SPACE or pygame.K_m:
        disparar(event, ai_settings, screen, stats, nave, disparos)
    if event.key == pygame.K_F11:
        pygame.display.toggle_fullscreen()
    if event.key == pygame.K_ESCAPE: 
        sys.exit()


def eventos_keyup(event, ai_settings, nave):
# Faz parte de eventos
    if event.key == pygame.K_RIGHT:
        nave.moving_right = False
    if event.key == pygame.K_LEFT:
        nave.moving_left = False
    if event.key == pygame.K_m:
        ai_settings.disparando = False


def checar_eventos(ai_settings, screen, nave, disparos, alienigenas, stats, tabelapontos, disparos_alienigenas, play_button):
# Responde as ações do usuário
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            eventos_keydown(event, ai_settings, screen, stats, nave, disparos)
        elif event.type == pygame.KEYUP:
            eventos_keyup(event, ai_settings, nave)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, nave, disparos, alienigenas, stats, play_button, tabelapontos, disparos_alienigenas, mouse_x, mouse_y)


def check_play_button(ai_settings, screen, nave, disparos, alienigenas, stats, play_button, tabelapontos, disparos_alienigenas, mouse_x, mouse_y):
# Faz parte de checar_eventos
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        ai_settings.initialize_dynamic_settings()
        pygame.mouse.set_visible(False)
        # Reinicia estatísticas
        stats.resetar_status()
        stats.game_active = True
        # Reinicia imagens do painel
        tabelapontos.prep_score()
        tabelapontos.prep_high_score()
        tabelapontos.prep_level()
        tabelapontos.prep_ships()
        # Tira alienigenas e nave
        alienigenas.empty()
        disparos.empty()
        disparos_alienigenas.empty()
        # Coloca alienigenas e nave
        ai_settings.alienigenas_bomba = False 
        criar_frota(ai_settings, screen, stats, nave, alienigenas) 
        nave.centrar_nave()
        # Som de start
        pygame.mixer.music.load('sons/game-start-6104.mp3')
        pygame.mixer.music.play()


def disparar(event, ai_settings, screen, stats, nave, disparos):
# Faz parte de eventos_keydown
    novo_disparo = Disparo(ai_settings, screen, nave)
    if len(disparos) < ai_settings.bullets_allowed and stats.game_active == True:
        if event.key == pygame.K_SPACE:
            disparos.add(novo_disparo)
            stats.bullet_shots += 1
        # teste
        elif event.key == pygame.K_m:
            disparos.add(novo_disparo)
            ai_settings.disparando = True


def desenhar_disparos(ai_settings, screen, nave, disparos, stats, disparos_alienigenas):
    # Desenha os projeteis, faz parte de atualizar_tela
    novo_disparo = Disparo(ai_settings, screen, nave) # teste
    for disparo in disparos.sprites(): 
        disparo.desenhar_disparo()
        if ai_settings.disparando == True and len(disparos) < ai_settings.bullets_allowed: # if ai_settings.disparando == True and len(disparos): # colocar esse if == bug legal # teste
            disparos.add(novo_disparo)
            stats.bullet_shots += 1
    for disparo_alienigena in disparos_alienigenas.sprites(): 
        disparo_alienigena.desenhar_disparo() # teste


def atualizar_tela(ai_settings, screen, nave, disparos, alienigenas, stats, play_button, tabelapontos, disparos_alienigenas):
# Atualiza as informações na tela
    screen.fill(ai_settings.bg_color)
    desenhar_disparos(ai_settings, screen, nave, disparos, stats, disparos_alienigenas) # Desenha os projeteis
    nave.mostrar() # Desenha a nave
    alienigenas.draw(screen) # Desenha o alienigena
    tabelapontos.show_score() # Desenha a tabela de pontos
    # Desenha o botão de play
    if not stats.game_active:
        play_button.desenhar_button()
    # Mostra a tela
    pygame.display.flip()


def adicionar_disparos_alienigenas(ai_settings, screen, stats, nave, alienigenas, disparos_alienigenas):
    # teste disparo, faz parte de atualizar_disparos
    alienigenas_valores = total_alienigenas(ai_settings, stats, nave, screen, alienigenas)
    for alien_move in alienigenas.sprites():
        if alien_move.checar_lados() and len(disparos_alienigenas) < ai_settings.alien_bullets_allowed:
            alien_number_x = alienigenas_valores['aliens_x']
            row_number_y = alienigenas_valores['aliens_y']
            novo_disparo_alienigena = Disparo_alienigena(ai_settings, screen, nave) 
            novo_disparo_alienigena.posicao_disparo(alienigenas, alien_number_x, row_number_y)
            if novo_disparo_alienigena.rect.x != 0 and novo_disparo_alienigena.y != 0: disparos_alienigenas.add(novo_disparo_alienigena) 


def checar_pontuacao_maxima(stats, tabelapontos):
# Faz parte de checar_colisao_alienigena_disparo
    if stats.score > stats.high_score: 
        stats.high_score = stats.score
        tabelapontos.prep_high_score()
        # Som de pontuação
        pygame.mixer.music.load('sons/recorde.wav')
        pygame.mixer.music.play()


def checar_colisao_alienigena_disparo(ai_settings, screen, disparos, alienigenas, nave, stats, tabelapontos, disparos_alienigenas):
# Remove os alienigenas que sofreram colisão # Faz parte de atualizar_disparo
    colisoes = pygame.sprite.groupcollide(disparos, alienigenas, True, True)
    if colisoes:
        for alienigenas in colisoes.values():
            stats.alienigenas_mortos += 1
            stats.score += ai_settings.alien_points * len(alienigenas)
            tabelapontos.prep_score()
            checar_pontuacao_maxima(stats, tabelapontos)
        # Som de pontuação
        pygame.mixer.music.load('sons/pickupCoin.wav')
        pygame.mixer.music.set_volume(0.75)
        pygame.mixer.music.play()
    # teste
    if pygame.sprite.spritecollideany(nave, disparos_alienigenas): 
        nave_colidir(ai_settings, screen, stats, nave, alienigenas, disparos, tabelapontos, disparos_alienigenas)


def atualizar_disparos(ai_settings, screen, disparos, alienigenas, nave, stats, tabelapontos, disparos_alienigenas):
# Atualiza os disparos e remove os disparos fora da tela
    for disparo in disparos.copy():
        if disparo.rect.bottom <= 0:
            disparos.remove(disparo)
    # teste
    for disparo_alienigena in disparos_alienigenas.copy():
        if disparo_alienigena.rect.top >= 800:
            disparos_alienigenas.remove(disparo_alienigena)
    adicionar_disparos_alienigenas(ai_settings, screen, stats, nave, alienigenas, disparos_alienigenas) # teste
    checar_colisao_alienigena_disparo(ai_settings, screen, disparos, alienigenas, nave, stats, tabelapontos, disparos_alienigenas)
    

def get_number_aliens_x(ai_settings, alien_width):
# Define quantos alienigenas cabem em uma linha # Faz parte de total_alienigenas
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))

    return number_aliens_x


def pegar_numero_linhas(ai_settings, ship_height, alien_height):
# Linhas com alienigenas que cabe na tela # Faz parte de total_alienigenas
    available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))

    return number_rows


def total_alienigenas(ai_settings, stats, nave, screen, alienigenas):
# Faz parte de checar_quantidade_alienigena
    alienigena = Alienigena(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alienigena.rect.width)
    number_rows_y = pegar_numero_linhas(ai_settings, nave.rect.height, alienigena.rect.height)
    
    if stats.level == 1 or stats.level == 2:
        number_rows_y = 1
    elif stats.level == 3 or stats.level == 4:
        number_rows_y = 2
    elif stats.level == 5 or stats.level == 6:
        number_rows_y = 3

    total_number_aliens = number_aliens_x * number_rows_y
    quantidade_alienigenas = len(alienigenas.sprites())
    alienigenas_valores = {
        'total_alienigenas': total_number_aliens,
        'quantidade_alienigenas': quantidade_alienigenas,
        'aliens_x': number_aliens_x,
        'aliens_y': number_rows_y
    }
    return alienigenas_valores


def criar_alienigena(ai_settings, screen, alienigenas, alien_number_x, row_number_y):
# Cria um alienigena # Faz parte de criar_frota
    alienigena = Alienigena(ai_settings, screen, alien_number_x, row_number_y)
    alien_width = alienigena.rect.width
    alienigena.x = alien_width + 2 * alien_width * alien_number_x 
    alienigena.rect.x = alienigena.x 
    alienigena.rect.y = alienigena.rect.height + 2 * alienigena.rect.height * row_number_y
    alienigenas.add(alienigena)

# teste
def criar_bomba(ai_settings, screen, alienigenas_bomba, alien_number_x, row_number_y):
# Cria um alienigena # Faz parte de criar_frota
    alienigena_bomba = Bomba(ai_settings, screen, alien_number_x, row_number_y)
    alien_width = alienigena_bomba.rect.width
    alienigena_bomba.x = alien_width + 2 * alien_width * alien_number_x 
    alienigena_bomba.rect.x = alienigena_bomba.x 
    alienigena_bomba.rect.y = alienigena_bomba.rect.height + 2 * alienigena_bomba.rect.height * row_number_y
    alienigenas_bomba.add(alienigena_bomba)
    

def criar_frota(ai_settings, screen, stats, nave, alienigenas):
# Cria uma frota de alienigenas # Faz parte de nave_colidir e checar_quantidade_alienigenas
    alienigenas_valores = total_alienigenas(ai_settings, stats, nave, screen, alienigenas)
    number_aliens_x = alienigenas_valores['aliens_x']
    number_rows_y = alienigenas_valores['aliens_y']

    if stats.level == 1 or stats.level == 2:
        number_rows_y = 1
    elif stats.level == 3 or stats.level == 4:
        number_rows_y = 2
    elif stats.level == 5 or stats.level == 6:
        number_rows_y = 3

    # teste
    if ai_settings.alienigenas == True: 
        for row_number_y in range(number_rows_y):
            for alien_number_x in range(number_aliens_x):
                criar_alienigena(ai_settings, screen, alienigenas, alien_number_x, row_number_y)
    elif ai_settings.alienigenas_bomba == True: 
        for row_number_y in range(number_rows_y):
            alien_number_x = randint(1, number_aliens_x)
            criar_bomba(ai_settings, screen, alienigenas, alien_number_x, row_number_y)


def mudar_movimento_frota(ai_settings, alien_move):
# Muda a direção de movimento da frota # Faz parte de checar_lados_frota
    alien_move.rect.y += ai_settings.fleet_drop_speed
    alien_move.alien_direction *= -1


def checar_lados_frota(ai_settings, alienigenas):
# Vê se algum dos alienigenas está tocando um dos lados # Faz parte de atualizar_alienigenas
    for alien_move in alienigenas.sprites(): 
        if alien_move.checar_lados():
            mudar_movimento_frota(ai_settings, alien_move)


def checar_fundo_tela(ai_settings, screen, stats, nave, alienigenas, disparos, tabelapontos, disparos_alienigenas):
# Faz parte de atualizar_alienigens
    screen_rect = screen.get_rect()
    for alienigena in alienigenas.sprites():
        if alienigena.rect.bottom >= screen_rect.bottom:
            nave_colidir(ai_settings, screen, stats, nave, alienigenas, disparos, tabelapontos, disparos_alienigenas)
            break


def nave_colidir(ai_settings, screen, stats, nave, alienigenas, disparos, tabelapontos, disparos_alienigenas):
# Faz parte de atualizar_alienigenas e checar_fundo_tela
    stats.ships_left -= 1
    tabelapontos.prep_ships()
    if stats.ships_left > 0:
        # Esvazia grupos
        alienigenas.empty()
        disparos.empty()
        disparos_alienigenas.empty()
        # Recomeça
        ai_settings.alien_speed_factor = ai_settings.alien_speed_in_stage_game 
        criar_frota(ai_settings, screen, stats, nave, alienigenas)
        nave.centrar_nave()
        sleep(0.5)
    else:
        stats.registrar_tabela_json()
        stats.registrar_partida()
        stats.game_active = False
        pygame.mouse.set_visible(True)
    if stats.ships_left != 1:
        som_colisao = pygame.mixer.music
        som_colisao.load('sons/collision.wav')
        som_colisao.play()


def atualizar_velocidade_alienigenas(ai_settings, quantidade_alienigenas, total_number_aliens):
    # Faz parte de checar_quantidade_alienigenas
    if quantidade_alienigenas <= (total_number_aliens * 0.9):
        ai_settings.alien_speed_factor = ai_settings.alien_speed_in_stage_game + 0.25
    elif quantidade_alienigenas <= (total_number_aliens * 0.75):
        ai_settings.alien_speed_factor = ai_settings.alien_speed_in_stage_game + 0.5
    elif quantidade_alienigenas <= (total_number_aliens * 0.5):
        ai_settings.alien_speed_factor = ai_settings.alien_speed_in_stage_game + 0.75
    elif quantidade_alienigenas <= (total_number_aliens * 0.25):
        ai_settings.alien_speed_factor = ai_settings.alien_speed_in_stage_game + 1
    elif quantidade_alienigenas <= (total_number_aliens * 0.1):
        ai_settings.alien_speed_factor = ai_settings.alien_speed_in_stage_game + 2
    elif quantidade_alienigenas == 1:
        ai_settings.alien_speed_factor = ai_settings.alien_speed_in_stage_game + 3


def checar_quantidade_alienigenas(ai_settings, screen, stats, nave, alienigenas, disparos, tabelapontos, disparos_alienigenas):
    # Faz parte de atualizar_alienigenas
    alienigenas_valores = total_alienigenas(ai_settings, stats, nave, screen, alienigenas)
    total_number_aliens = alienigenas_valores['total_alienigenas']
    quantidade_alienigenas = alienigenas_valores['quantidade_alienigenas']
    atualizar_velocidade_alienigenas(ai_settings, quantidade_alienigenas, total_number_aliens)

    if len(alienigenas) == 0 and ai_settings.alienigenas == False and ai_settings.alienigenas_bomba == False: # teste
        ai_settings.alienigenas = True
        criar_frota(ai_settings, screen, stats, nave, alienigenas)
    elif len(alienigenas) == 0 and ai_settings.alienigenas == True and ai_settings.alienigenas_bomba == False: # teste
        ai_settings.alienigenas = False
        ai_settings.alienigenas_bomba = True
        criar_frota(ai_settings, screen, stats, nave, alienigenas)
    elif len(alienigenas) == 0 and ai_settings.alienigenas_bomba == True: # teste
        # Esvazia grupos
        alienigenas.empty()
        disparos.empty()
        disparos_alienigenas.empty()
        ai_settings.increase_speed()
        stats.level += 1 # Aumenta o level
        tabelapontos.prep_level()
        ai_settings.alien_speed_factor = ai_settings.alien_speed_in_stage_game 
        ai_settings.alienigenas_bomba = False # teste
        criar_frota(ai_settings, screen, stats, nave, alienigenas)
        

def atualizar_alienigenas(ai_settings, stats, screen, nave, alienigenas, disparos, tabelapontos, disparos_alienigenas):
    checar_quantidade_alienigenas(ai_settings, screen, stats, nave, alienigenas, disparos, tabelapontos, disparos_alienigenas) 
    checar_lados_frota(ai_settings, alienigenas)
    # Verifica se houve colisão com a nave
    if pygame.sprite.spritecollideany(nave, alienigenas): 
        nave_colidir(ai_settings, screen, stats, nave, alienigenas, disparos, tabelapontos, disparos_alienigenas)
    checar_fundo_tela(ai_settings, screen, stats, nave, alienigenas, disparos, tabelapontos, disparos_alienigenas)
