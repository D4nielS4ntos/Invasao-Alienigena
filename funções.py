import sys
import time
from time import sleep
from random import randint, choice
import json

import pygame

from classes.disparo import Disparo, Disparo_alienigena
from classes.alienigena import Alienigena
from classes.bomba import Bomba


def write_name(ai_settings, stats, table_of_points, event, input):
# Faz parte de events
    if stats.game_active == False and ai_settings.aliens == False and ai_settings.bombs == False and ai_settings.questions == False:
        if event.key == pygame.K_q:
            input = input + "q"
        elif event.key == pygame.K_w:
            input = input + "w"
        elif event.key == pygame.K_e:
            input = input + "e"
        elif event.key == pygame.K_r:
            input = input + "r"
        elif event.key == pygame.K_t:
            input = input + "t"
        elif event.key == pygame.K_y:
            input = input + "y"
        elif event.key == pygame.K_u:
            input = input + "u"
        elif event.key == pygame.K_i:
            input = input + "i"
        elif event.key == pygame.K_o:
            input = input + "o"
        elif event.key == pygame.K_p:
            input = input + "p"
        elif event.key == pygame.K_a:
            input = input + "a"
        elif event.key == pygame.K_s:
            input = input + "s"
        elif event.key == pygame.K_d:
            input = input + "d"
        elif event.key == pygame.K_f:
            input = input + "f"
        elif event.key == pygame.K_g:
            input = input + "g"
        elif event.key == pygame.K_h:
            input = input + "h"
        elif event.key == pygame.K_j:
            input = input + "j"
        elif event.key == pygame.K_k:
            input = input + "k"
        elif event.key == pygame.K_l:
            input = input + "l"
        elif event.key == pygame.K_z:
            input = input + "z"
        elif event.key == pygame.K_x:
            input = input + "x"
        elif event.key == pygame.K_c:
            input = input + "c"
        elif event.key == pygame.K_v:
            input = input + "v"
        elif event.key == pygame.K_b:
            input = input + "b"
        elif event.key == pygame.K_n:
            input = input + "n"
        elif event.key == pygame.K_m:
            input = input + "m"
        elif event.key == pygame.K_1:
            input = input + "1"
        elif event.key == pygame.K_2:
            input = input + "2"
        elif event.key == pygame.K_3:
            input = input + "3"
        elif event.key == pygame.K_4:
            input = input + "4"
        elif event.key == pygame.K_5:
            input = input + "5"
        elif event.key == pygame.K_6:
            input = input + "6"
        elif event.key == pygame.K_7:
            input = input + "7"
        elif event.key == pygame.K_8:
            input = input + "8"
        elif event.key == pygame.K_9:
            input = input + "9"
        elif event.key == pygame.K_0:
            input = input + "0"
    else:
        pass
    stats.name = input
    table_of_points.prep_name()


def pause(event, ai_settings, stats):
# Faz parte de keydown_events
    if stats.initial_time != 0 and ai_settings.writen_name == True and stats.name != 'digite seu nome...':
        if event.key == pygame.K_p and stats.game_active == True:
            pygame.mouse.set_visible(True)
            stats.game_active = False
        elif event.key == pygame.K_p and stats.game_active == False:
            pygame.mouse.set_visible(False)
            stats.game_active = True


def keydown_events(event, ai_settings, screen, stats, ship, shots): 
# Faz parte de events
    if event.key == pygame.K_RIGHT: 
        ship.moving_right = True
    if event.key == pygame.K_LEFT: 
        ship.moving_left = True
    if event.key == pygame.K_SPACE or pygame.K_m:
        shoting(event, ai_settings, screen, stats, ship, shots)
    if event.key == pygame.K_p:
        pause(event, ai_settings, stats)
    if event.key == pygame.K_F11:
        pygame.display.toggle_fullscreen()
    if event.key == pygame.K_ESCAPE: 
        sys.exit()


def keyup_events(event, ai_settings, ship):
# Faz parte de events
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    if event.key == pygame.K_LEFT:
        ship.moving_left = False
    if event.key == pygame.K_m:
        ai_settings.shoting = False


def events(ai_settings, screen, ship, shots, aliens, alien_bombs, stats, table_of_points, shots_aliens, play_button):
# Responde as ações do usuário
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            keydown_events(event, ai_settings, screen, stats, ship, shots)
            write_name(ai_settings, stats, table_of_points, event, stats.name)
        elif event.type == pygame.KEYUP:
            keyup_events(event, ai_settings, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, ship, shots, aliens, alien_bombs, stats, play_button, table_of_points, shots_aliens, mouse_x, mouse_y)


def check_play_button(ai_settings, screen, ship, shots, aliens, alien_bombs, stats, play_button, table_of_points, shots_aliens, mouse_x, mouse_y):
# Faz parte de checar_eventos
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active and ai_settings.aliens == False and ai_settings.bombs == False and ai_settings.questions == False and ai_settings.writen_name == True and stats.name != 'digite seu nome...':
        ai_settings.initialize_dynamic_settings()
        pygame.mouse.set_visible(False)
        # Reinicia estatísticas
        stats.reset_stats()
        stats.game_active = True
        stats.initial_time = round(time.time(), 2)
        # Reinicia imagens do painel
        table_of_points.prep_score()
        table_of_points.prep_high_score()
        table_of_points.prep_level()
        table_of_points.prep_ships()
        table_of_points.prep_name()
        table_of_points.prep_timer()
        table_of_points.prep_question()
        table_of_points.prep_answers()
        # Tira aliens e ship
        aliens.empty()
        alien_bombs.empty()
        shots.empty()
        shots_aliens.empty()
        ai_settings.death_ray = False
        # Coloca aliens e ship
        create_fleet(ai_settings, screen, stats, ship, aliens, alien_bombs) 
        ship.center_ship()
        # Som de start
        pygame.mixer.music.load('sons/game-start-6104.mp3')
        pygame.mixer.music.play()
    elif button_clicked and not stats.game_active and ai_settings.aliens == True or ai_settings.bombs == True or ai_settings.questions == True and ai_settings.writen_name == True and stats.name != 'digite seu nome...':
        pygame.mouse.set_visible(False)
        stats.game_active = True


def shoting(event, ai_settings, screen, stats, ship, shots):
# Faz parte de keydown_events
    new_shot = Disparo(ai_settings, screen, ship)
    if len(shots) < ai_settings.bullets_allowed and stats.game_active == True:
        if event.key == pygame.K_SPACE:
            shots.add(new_shot)
            stats.bullet_shots += 1
        # teste
        elif event.key == pygame.K_m:
            shots.add(new_shot)
            ai_settings.shoting = True


def drawn_shots(ai_settings, screen, ship, shots, stats, shots_aliens):
    # Desenha os projeteis, faz parte de update_screen
    new_shot = Disparo(ai_settings, screen, ship) # teste
    for shot in shots.sprites(): 
        shot.drawn_shot(ship)
        if ai_settings.shoting == True and len(shots) < ai_settings.bullets_allowed: # if ai_settings.shoting == True and len(shots): # colocar esse if == bug legal # teste
            shots.add(new_shot)
            stats.bullet_shots += 1
    for shot_alien in shots_aliens.sprites(): 
        shot_alien.drawn_shot() # teste


def screen_update(ai_settings, screen, ship, shots, aliens, alien_bombs, stats, play_button, table_of_points, shots_aliens, mother_ship):
# Atualiza as informações na tela
    screen.fill(ai_settings.bg_color)
    drawn_shots(ai_settings, screen, ship, shots, stats, shots_aliens) # Desenha os projeteis
    ship.show() # Desenha a ship
    aliens.draw(screen) # Desenha o alien
    alien_bombs.draw(screen) # Desenha o alien
    table_of_points.show_score() # Desenha a tabela de pontos
    stats.current_time = round(time.time(), 2)
    table_of_points.prep_timer()
    if ai_settings.questions == True:
        mother_ship.show() # Desenha a nave mãe
    elif ai_settings.death_ray == True and stats.ships_left == 0:
        mother_ship.show() # Desenha a nave mãe
        pygame.draw.line(screen, ai_settings.alien_bullet_color, (mother_ship.rect_mother_ship.centerx, mother_ship.rect_mother_ship.centery), (ship.rect.centerx, ship.rect.centery), 5)
    # Desenha o botão de play
    if not stats.game_active:
        play_button.drawn_button()
    # Mostra a tela
    pygame.display.flip()


def add_alien_shots(ai_settings, screen, stats, ship, aliens, shots_aliens):
    # teste shot, faz parte de update_shots
    alien_values = total_aliens(ai_settings, stats, ship, screen, aliens)
    for alien_move in aliens.sprites():
        if alien_move.check_sides() and len(shots_aliens) < ai_settings.alien_bullets_allowed:
            alien_number_x = alien_values['aliens_x']
            row_number_y = alien_values['aliens_y']
            novo_shot_alien = Disparo_alienigena(ai_settings, screen, ship) 
            novo_shot_alien.shot_position(aliens, alien_number_x, row_number_y)
            if novo_shot_alien.rect.x != 0 and novo_shot_alien.y != 0: 
                shots_aliens.add(novo_shot_alien) 


def check_high_score(stats, table_of_points):
# Faz parte de check_alien_shot_collision
    if stats.score > stats.high_score: 
        # Registrar nome do recorde
        stats.high_score = stats.score
        stats.high_score_name = stats.name.upper()
        table_of_points.prep_high_score()
        json_arquive = open('tabela.json')
        json_table = json.load(json_arquive)
        stats.second_high_score_name = json_table['placar'][-2]['pontuacao_maxima_nome']
        stats.third_high_score_name = json_table['placar'][-3]['pontuacao_maxima_nome']
        stats.second_high_score = json_table['placar'][-2]['pontuacao_maxima']
        stats.third_high_score = json_table['placar'][-3]['pontuacao_maxima']
        # Som de pontuação
        pygame.mixer.music.load('sons/recorde.wav')
        pygame.mixer.music.set_volume(0.25)
        pygame.mixer.music.play()
    elif stats.score > stats.second_high_score: 
        # Registrar nome do recorde
        stats.second_high_score = stats.score
        stats.second_high_score_name = stats.name.upper()
        json_arquive = open('tabela.json')
        json_table = json.load(json_arquive)
        stats.third_high_score_name = json_table['placar'][-3]['pontuacao_maxima_nome']
        stats.third_high_score = json_table['placar'][-3]['pontuacao_maxima']
        table_of_points.prep_high_score()
        # Som de pontuação
        pygame.mixer.music.load('sons/recorde.wav')
        pygame.mixer.music.set_volume(0.25)
        pygame.mixer.music.play()
    elif stats.score > stats.third_high_score: 
        # Registrar nome do recorde
        stats.third_high_score = stats.score
        stats.third_high_score_name = stats.name.upper()
        table_of_points.prep_high_score()
        # Som de pontuação
        pygame.mixer.music.load('sons/recorde.wav')
        pygame.mixer.music.set_volume(0.25)
        pygame.mixer.music.play()


def shot_collision(shots, stats, table_of_points, enemy, enemy_points):
# Faz parte de check_alien_shot_collision
    colisoes = pygame.sprite.groupcollide(shots, enemy, True, True)
    if colisoes:
        for enemy in colisoes.values():
            stats.alien_deaths += 1
            stats.score += enemy_points * len(enemy)
            table_of_points.prep_score()
            check_high_score(stats, table_of_points)
        if stats.score <= stats.high_score: 
            # Som de pontuação
            pygame.mixer.music.load('sons/pickupCoin.wav')
            pygame.mixer.music.set_volume(0.75)
            pygame.mixer.music.play()


def check_alien_shot_collision(ai_settings, screen, shots, aliens, alien_bombs, ship, stats, table_of_points, shots_aliens):
# Remove os aliens que sofreram colisão # Faz parte de shots_update
    shot_collision(shots, stats, table_of_points, aliens, ai_settings.alien_points)
    shot_collision(shots, stats, table_of_points, alien_bombs, ai_settings.bomb_points)
    if pygame.sprite.spritecollideany(ship, shots_aliens): 
        collide_ship(ai_settings, screen, stats, ship, aliens, alien_bombs, shots, table_of_points, shots_aliens)


def shots_update(ai_settings, screen, shots, aliens, alien_bombs, ship, stats, table_of_points, shots_aliens):
# Atualiza os shots e remove os shots fora da tela
    for shot in shots.copy():
        if shot.rect.bottom <= 0 or shot.rect.top >= ai_settings.screen_height:
            shots.remove(shot)
    # teste
    for shot_alien in shots_aliens.copy():
        if shot_alien.rect.top >= 800:
            shots_aliens.remove(shot_alien)
    add_alien_shots(ai_settings, screen, stats, ship, aliens, shots_aliens)
    check_alien_shot_collision(ai_settings, screen, shots, aliens, alien_bombs, ship, stats, table_of_points, shots_aliens)
    

def get_number_aliens_line_x(ai_settings, alien_width):
# Define quantos aliens cabem em uma linha # Faz parte de total_aliens
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))

    return number_aliens_x


def get_number_aliens_row_y(ai_settings, ship_height, alien_height):
# Linhas com aliens que cabe na tela # Faz parte de total_aliens
    available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
    number_aliens_y = int(available_space_y / (2 * alien_height))

    return number_aliens_y


def total_aliens(ai_settings, stats, ship, screen, aliens):
# Faz parte de checar_quantidade_alien
    alien = Alienigena(ai_settings, screen)
    number_aliens_x = get_number_aliens_line_x(ai_settings, alien.rect.width)
    number_aliens_y = get_number_aliens_row_y(ai_settings, ship.rect.height, alien.rect.height)
    
    if stats.level == 1 or stats.level == 2:
        number_aliens_y = 1
    elif stats.level == 3 or stats.level == 4:
        number_aliens_y = 2
    elif stats.level == 5 or stats.level == 6:
        number_aliens_y = 3

    total_number_aliens = number_aliens_x * number_aliens_y
    aliens_quantity = len(aliens.sprites())
    aliens_valores = {
        'total_aliens': total_number_aliens,
        'alien_quantity': aliens_quantity,
        'aliens_x': number_aliens_x,
        'aliens_y': number_aliens_y
    }
    return aliens_valores


def create_alien(ai_settings, screen, aliens, alien_number_x, row_number_y):
# Cria um alien # Faz parte de create_fleet
    alien = Alienigena(ai_settings, screen, alien_number_x, row_number_y)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number_x 
    alien.rect.x = alien.x 
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number_y
    aliens.add(alien)

# teste
def create_bomb(ai_settings, screen, alien_bombs, alien_number_x, row_number_y, ship):
# Cria um alien # Faz parte de create_fleet
    alien_bomb = Bomba(ai_settings, screen, ship, alien_number_x, row_number_y)
    alien_width = alien_bomb.rect.width
    alien_bomb.x = alien_width + 2 * alien_width * alien_number_x 
    alien_bomb.rect.x = alien_bomb.x 
    alien_bomb.rect.y = alien_bomb.rect.height + 2 * alien_bomb.rect.height * row_number_y
    alien_bombs.add(alien_bomb)
    

def create_fleet(ai_settings, screen, stats, ship, aliens, alien_bombs):
# Cria uma frota de aliens # Faz parte de collide_ship e check_alien_quantity
    aliens_valores = total_aliens(ai_settings, stats, ship, screen, aliens)
    number_aliens_x = aliens_valores['aliens_x']
    number_aliens_y = aliens_valores['aliens_y']
    # Atualiza fileiras
    if stats.level == 1 or stats.level == 2:
        number_aliens_y = 1
    elif stats.level == 3 or stats.level == 4:
        number_aliens_y = 2
    elif stats.level == 5 or stats.level == 6:
        number_aliens_y = 3
    # Cria a frota
    if ai_settings.aliens == True:
        for row_number_y in range(number_aliens_y):
            for alien_number_x in range(number_aliens_x):
                create_alien(ai_settings, screen, aliens, alien_number_x, row_number_y)
    elif ai_settings.bombs == True: 
        alien_number_x = randint(0, 15)
        row_number_y = 0 
        create_bomb(ai_settings, screen, alien_bombs, alien_number_x, row_number_y, ship)
        ai_settings.bombs_in_stage += 1


def change_fleet_movement(ai_settings, alien_move):
# Muda a direção de movimento da frota # Faz parte de check_fleet_sides
    alien_move.rect.y += ai_settings.fleet_drop_speed
    alien_move.alien_direction *= -1


def check_fleet_sides(ai_settings, aliens, mother_ship):
# Vê se algum dos aliens está tocando um dos lados # Faz parte de aliens_update
    for alien_move in aliens.sprites(): 
        if alien_move.check_sides():
            change_fleet_movement(ai_settings, alien_move)
    if mother_ship.check_sides():
        mother_ship.direction *= -1


def check_screen_botton(ai_settings, screen, stats, ship, aliens, alien_bombs, shots, table_of_points, shots_aliens):
# Faz parte de aliens_update
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            collide_ship(ai_settings, screen, stats, ship, aliens, shots, table_of_points, shots_aliens)
            break
    for bomb in alien_bombs.sprites():
        if bomb.rect.bottom >= screen_rect.bottom:
            alien_bombs.remove(bomb)


def collide_ship(ai_settings, screen, stats, ship, aliens, alien_bombs, shots, table_of_points, shots_aliens):
# Faz parte de aliens_update e check_screen_botton
    stats.ships_left -= 1
    table_of_points.prep_ships()
    if stats.ships_left > 0:
        # Esvazia grupos
        aliens.empty()
        alien_bombs.empty()
        shots.empty()
        shots_aliens.empty()
        # Recomeça
        ai_settings.alien_speed_factor = ai_settings.alien_speed_in_stage_game 
        create_fleet(ai_settings, screen, stats, ship, aliens, alien_bombs)
        ship.center_ship()
        sleep(0.5)
    elif stats.name == 'digite seu nome...':
        print('ERRO aahh')
    else:
        ship.image = pygame.image.load('imagens/explosão.png')
        stats.register_json_table()
        stats.play_register()
        stats.game_active = False
        ai_settings.aliens = False
        ai_settings.bombs = False
        ai_settings.questions = False
        ai_settings.answer = False
        ai_settings.writen_name = False
        stats.name = 'digite seu nome...'
        table_of_points.prep_name()
        pygame.mouse.set_visible(True)
    if stats.ships_left != 1:
        som_colisao = pygame.mixer.music
        som_colisao.load('sons/collision.wav')
        som_colisao.play()


def update_alien_speed(ai_settings, alien_quantity, total_number_aliens):
# Faz parte de check_alien_quantity
    if ai_settings.aliens == True:
        if alien_quantity <= (total_number_aliens * 0.9) and ai_settings.alien_speed_factor <= ai_settings.alien_speed_in_stage_game + 0.25:
            ai_settings.alien_speed_factor = ai_settings.alien_speed_in_stage_game + 0.5
        elif alien_quantity <= (total_number_aliens * 0.75) and ai_settings.alien_speed_factor <= ai_settings.alien_speed_in_stage_game + 0.5:
            ai_settings.alien_speed_factor = ai_settings.alien_speed_in_stage_game + 1
        elif alien_quantity <= (total_number_aliens * 0.5) and ai_settings.alien_speed_factor <= ai_settings.alien_speed_in_stage_game + 0.75:
            ai_settings.alien_speed_factor = ai_settings.alien_speed_in_stage_game + 1.5
        elif alien_quantity <= (total_number_aliens * 0.25) and ai_settings.alien_speed_factor <= ai_settings.alien_speed_in_stage_game + 1:
            ai_settings.alien_speed_factor = ai_settings.alien_speed_in_stage_game + 2
        elif alien_quantity <= (total_number_aliens * 0.1) and alien_quantity != 1 and ai_settings.alien_speed_factor <= ai_settings.alien_speed_in_stage_game + 2:
            ai_settings.alien_speed_factor = ai_settings.alien_speed_in_stage_game + 3
        elif alien_quantity == 1 and ai_settings.alien_speed_factor <= ai_settings.alien_speed_in_stage_game + 3:
            ai_settings.alien_speed_factor = ai_settings.alien_speed_in_stage_game + 5


def check_alien_quantity(ai_settings, screen, stats, ship, aliens, alien_bombs, shots, table_of_points, shots_aliens):
# Faz parte de aliens_update
    alien_values = total_aliens(ai_settings, stats, ship, screen, aliens)
    total_number_aliens = alien_values['total_aliens']
    alien_quantity = alien_values['alien_quantity']
    update_alien_speed(ai_settings, alien_quantity, total_number_aliens)

    if len(aliens) == 0 and ai_settings.aliens == False and ai_settings.bombs == False and ai_settings.questions == False and ai_settings.answer == False: 
        # Criar aliens
        ai_settings.aliens = True
        create_fleet(ai_settings, screen, stats, ship, aliens, alien_bombs)
    elif len(aliens) == 0 and ai_settings.aliens == True and ai_settings.bombs == False and ai_settings.questions == False and ai_settings.answer == False: 
        # Criar bombas
        ai_settings.aliens = False
        ai_settings.bombs = True
        create_fleet(ai_settings, screen, stats, ship, aliens, alien_bombs)
    elif len(aliens) == 0 and len(alien_bombs) == 0 and ai_settings.bombs_in_stage <= ai_settings.level and ai_settings.aliens == False and ai_settings.bombs == True and ai_settings.questions == False and ai_settings.answer == False:
        # Criar bombas
        create_fleet(ai_settings, screen, stats, ship, aliens, alien_bombs)
    elif len(aliens) == 0 and len(alien_bombs) == 0 and ai_settings.bombs_in_stage >= ai_settings.level and ai_settings.aliens == False and ai_settings.bombs == True and ai_settings.questions == False and ai_settings.answer == False:
        ai_settings.bombs = False 
        ai_settings.questions = True
    elif len(aliens) == 0 and len(alien_bombs) == 0 and ai_settings.bombs_in_stage >= ai_settings.level and ai_settings.aliens == False and ai_settings.bombs == False and ai_settings.questions == False and ai_settings.answer == True:
        # Esvazia grupos
        ai_settings.answer = False
        if ai_settings.death_ray == True:
            ai_settings.death_ray = False
        ai_settings.bombs_in_stage = 0
        aliens.empty()
        shots.empty()
        shots_aliens.empty()
        ai_settings.increase_speed()
        stats.level += 1 # Aumenta o level
        table_of_points.prep_level()
        ai_settings.alien_speed_factor = ai_settings.alien_speed_in_stage_game 


def check_question(ai_settings, screen, stats, ship, aliens, alien_bombs, shots, table_of_points, shots_aliens, mother_ship, question):
# Faz parte parte de collede_questions
    resposta = f'resposta_{question.upper()}'
    if stats.json_questions_table['perguntas'][stats.current_question][resposta] == stats.json_questions_table['perguntas'][stats.current_question]['resposta_correta']:
        ai_settings.questions = False
        ai_settings.answer = True
        ai_settings.time_of_question = False
        som_right_answer = pygame.mixer.music
        som_right_answer.load('sons/right_answer.wav')
        som_right_answer.play()
        # Trocar pergunta
        if len(stats.list_numbers_of_questions) == 1:
            stats.reset_questions()
        else:
            stats.list_numbers_of_questions.remove(stats.current_question)
            stats.current_question = choice(stats.list_numbers_of_questions)
        table_of_points.prep_question()
        table_of_points.prep_answers()
    else:
        ai_settings.death_ray = True
        pygame.draw.line(screen, ai_settings.alien_bullet_color, (mother_ship.rect_mother_ship.centerx, mother_ship.rect_mother_ship.centery), (ship.rect.centerx, ship.rect.centery), 5)
        pygame.display.update()
        collide_ship(ai_settings, screen, stats, ship, aliens, alien_bombs, shots, table_of_points, shots_aliens)


def collide_questions(ai_settings, screen, stats, ship, aliens, alien_bombs, shots, table_of_points, shots_aliens, mother_ship):
# Faz parte de aliens_update
    for shot in shots:
        if pygame.Rect.colliderect(shot.rect, mother_ship.rect_mother_ship):
            shot.speed_factor *= -1
            # mudar depois
            # Som de pontuação
            pygame.mixer.music.load('sons/pickupCoin.wav')
            pygame.mixer.music.set_volume(0.75)
            pygame.mixer.music.play()
        elif pygame.Rect.colliderect(shot.rect, mother_ship.qa_rect):
            check_question(ai_settings, screen, stats, ship, aliens, alien_bombs, shots, table_of_points, shots_aliens, mother_ship, 'A')
            break
        elif pygame.Rect.colliderect(shot.rect, mother_ship.qb_rect):
            check_question(ai_settings, screen, stats, ship, aliens, alien_bombs, shots, table_of_points, shots_aliens, mother_ship, 'B')
            break
        elif pygame.Rect.colliderect(shot.rect, mother_ship.qc_rect):
            check_question(ai_settings, screen, stats, ship, aliens, alien_bombs, shots, table_of_points, shots_aliens, mother_ship, 'C')
            break
        elif pygame.Rect.colliderect(shot.rect, mother_ship.qd_rect):
            check_question(ai_settings, screen, stats, ship, aliens, alien_bombs, shots, table_of_points, shots_aliens, mother_ship, 'D')
            break


def aliens_update(ai_settings, stats, screen, ship, aliens, alien_bombs, shots, table_of_points, shots_aliens, mother_ship):
    check_alien_quantity(ai_settings, screen, stats, ship, aliens, alien_bombs, shots, table_of_points, shots_aliens) 
    check_fleet_sides(ai_settings, aliens, mother_ship)
    # Verifica se houve colisão com a ship
    if pygame.sprite.spritecollideany(ship, aliens) or pygame.sprite.spritecollideany(ship, alien_bombs): 
        collide_ship(ai_settings, screen, stats, ship, aliens, alien_bombs, shots, table_of_points, shots_aliens)
    if ai_settings.questions:
        collide_questions(ai_settings, screen, stats, ship, aliens, alien_bombs, shots, table_of_points, shots_aliens, mother_ship)
    check_screen_botton(ai_settings, screen, stats, ship, aliens, alien_bombs, shots, table_of_points, shots_aliens)
