import sys
from time import sleep
from random import randint

import pygame

from classes.disparo import Disparo, Disparo_alienigena
from classes.alienigena import Alienigena
from classes.bomba import Bomba


def keydown_events(event, ai_settings, screen, stats, ship, shots): 
# Faz parte de events
    if event.key == pygame.K_RIGHT: 
        ship.moving_right = True
    if event.key == pygame.K_LEFT: 
        ship.moving_left = True
    if event.key == pygame.K_SPACE or pygame.K_m:
        shoting(event, ai_settings, screen, stats, ship, shots)
    if event.key == pygame.K_p:
        stats.game_active = False
        pygame.mouse.set_visible(True)
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


def events(ai_settings, screen, ship, shots, aliens, stats, table_of_points, shots_aliens, play_button):
# Responde as ações do usuário
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            keydown_events(event, ai_settings, screen, stats, ship, shots)
        elif event.type == pygame.KEYUP:
            keyup_events(event, ai_settings, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, ship, shots, aliens, stats, play_button, table_of_points, shots_aliens, mouse_x, mouse_y)


def check_play_button(ai_settings, screen, ship, shots, aliens, stats, play_button, table_of_points, shots_aliens, mouse_x, mouse_y):
# Faz parte de checar_eventos
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active and ai_settings.aliens == False and ai_settings.bombs == False:
        ai_settings.initialize_dynamic_settings()
        pygame.mouse.set_visible(False)
        # Reinicia estatísticas
        stats.reset_stats()
        stats.game_active = True
        # Reinicia imagens do painel
        table_of_points.prep_score()
        table_of_points.prep_high_score()
        table_of_points.prep_level()
        table_of_points.prep_ships()
        # Tira aliens e ship
        aliens.empty()
        shots.empty()
        shots_aliens.empty()
        # Coloca aliens e ship
        create_fleet(ai_settings, screen, stats, ship, aliens) 
        ship.center_ship()
        # Som de start
        pygame.mixer.music.load('sons/game-start-6104.mp3')
        pygame.mixer.music.play()
    elif button_clicked and not stats.game_active and ai_settings.aliens == True or ai_settings.bombs == True:
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


def screen_update(ai_settings, screen, ship, shots, aliens, stats, play_button, table_of_points, shots_aliens):
# Atualiza as informações na tela
    screen.fill(ai_settings.bg_color)
    drawn_shots(ai_settings, screen, ship, shots, stats, shots_aliens) # Desenha os projeteis
    ship.show() # Desenha a ship
    aliens.draw(screen) # Desenha o alien
    table_of_points.show_score() # Desenha a tabela de pontos
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
            if novo_shot_alien.rect.x != 0 and novo_shot_alien.y != 0: shots_aliens.add(novo_shot_alien) 


def check_high_score(stats, table_of_points):
# Faz parte de check_alien_shot_collision
    if stats.score > stats.high_score: 
        stats.high_score = stats.score
        table_of_points.prep_high_score()
        # Som de pontuação
        pygame.mixer.music.load('sons/recorde.wav')
        pygame.mixer.music.play()


def check_alien_shot_collision(ai_settings, screen, shots, aliens, ship, stats, table_of_points, shots_aliens):
# Remove os aliens que sofreram colisão # Faz parte de shots_update
    colisoes = pygame.sprite.groupcollide(shots, aliens, True, True)
    if colisoes:
        for aliens in colisoes.values():
            stats.alien_deaths += 1
            stats.score += ai_settings.alien_points * len(aliens)
            table_of_points.prep_score()
            check_high_score(stats, table_of_points)
        # Som de pontuação
        pygame.mixer.music.load('sons/pickupCoin.wav')
        pygame.mixer.music.set_volume(0.75)
        pygame.mixer.music.play()
    # teste
    if pygame.sprite.spritecollideany(ship, shots_aliens): 
        collide_ship(ai_settings, screen, stats, ship, aliens, shots, table_of_points, shots_aliens)


def shots_update(ai_settings, screen, shots, aliens, ship, stats, table_of_points, shots_aliens):
# Atualiza os shots e remove os shots fora da tela
    for shot in shots.copy():
        if shot.rect.bottom <= 0:
            shots.remove(shot)
    # teste
    for shot_alien in shots_aliens.copy():
        if shot_alien.rect.top >= 800:
            shots_aliens.remove(shot_alien)
    add_alien_shots(ai_settings, screen, stats, ship, aliens, shots_aliens) # teste
    check_alien_shot_collision(ai_settings, screen, shots, aliens, ship, stats, table_of_points, shots_aliens)
    

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
def create_bomb(ai_settings, screen, aliens_bomba, alien_number_x, row_number_y):
# Cria um alien # Faz parte de create_fleet
    alien_bomba = Bomba(ai_settings, screen, alien_number_x, row_number_y)
    alien_width = alien_bomba.rect.width
    alien_bomba.x = alien_width + 2 * alien_width * alien_number_x 
    alien_bomba.rect.x = alien_bomba.x 
    alien_bomba.rect.y = alien_bomba.rect.height + 2 * alien_bomba.rect.height * row_number_y
    aliens_bomba.add(alien_bomba)
    

def create_fleet(ai_settings, screen, stats, ship, aliens):
# Cria uma frota de aliens # Faz parte de collide_ship e check_alien_quantity
    aliens_valores = total_aliens(ai_settings, stats, ship, screen, aliens)
    number_aliens_x = aliens_valores['aliens_x']
    number_aliens_y = aliens_valores['aliens_y']

    if stats.level == 1 or stats.level == 2:
        number_aliens_y = 1
    elif stats.level == 3 or stats.level == 4:
        number_aliens_y = 2
    elif stats.level == 5 or stats.level == 6:
        number_aliens_y = 3

    # teste
    if ai_settings.aliens == True: 
        for row_number_y in range(number_aliens_y):
            for alien_number_x in range(number_aliens_x):
                create_alien(ai_settings, screen, aliens, alien_number_x, row_number_y)
    elif ai_settings.bombs == True: 
        # for row_number_y in range(number_aliens_y):
        row_number_y = 0
        alien_number_x = randint(1, number_aliens_x)
        create_bomb(ai_settings, screen, aliens, alien_number_x, row_number_y)


def change_fleet_movement(ai_settings, alien_move):
# Muda a direção de movimento da frota # Faz parte de check_fleet_sides
    alien_move.rect.y += ai_settings.fleet_drop_speed
    alien_move.alien_direction *= -1


def check_fleet_sides(ai_settings, aliens):
# Vê se algum dos aliens está tocando um dos lados # Faz parte de aliens_update
    for alien_move in aliens.sprites(): 
        if alien_move.check_sides():
            change_fleet_movement(ai_settings, alien_move)


def check_screen_botton(ai_settings, screen, stats, ship, aliens, shots, table_of_points, shots_aliens):
# Faz parte de aliens_update
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            collide_ship(ai_settings, screen, stats, ship, aliens, shots, table_of_points, shots_aliens)
            break


def collide_ship(ai_settings, screen, stats, ship, aliens, shots, table_of_points, shots_aliens):
# Faz parte de aliens_update e check_screen_botton
    stats.ships_left -= 1
    table_of_points.prep_ships()
    if stats.ships_left > 0:
        # Esvazia grupos
        aliens.empty()
        shots.empty()
        shots_aliens.empty()
        # Recomeça
        ai_settings.alien_speed_factor = ai_settings.alien_speed_in_stage_game 
        create_fleet(ai_settings, screen, stats, ship, aliens)
        ship.center_ship()
        sleep(0.5)
    else:
        ship.image = pygame.image.load('imagens/Explosão.png')
        stats.register_json_table()
        stats.play_register()
        stats.game_active = False
        ai_settings.aliens = False 
        ai_settings.aliens_bomba = False 
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


def check_alien_quantity(ai_settings, screen, stats, ship, aliens, shots, table_of_points, shots_aliens):
    # Faz parte de aliens_update
    alien_values = total_aliens(ai_settings, stats, ship, screen, aliens)
    total_number_aliens = alien_values['total_aliens']
    alien_quantity = alien_values['alien_quantity']
    update_alien_speed(ai_settings, alien_quantity, total_number_aliens)

    if len(aliens) == 0 and ai_settings.aliens == False and ai_settings.bombs == False: # teste
        ai_settings.aliens = True
        create_fleet(ai_settings, screen, stats, ship, aliens)
    elif len(aliens) == 0 and ai_settings.aliens == True and ai_settings.bombs == False: # teste
        ai_settings.aliens = False
        ai_settings.bombs = True
        create_fleet(ai_settings, screen, stats, ship, aliens)
    elif len(aliens) == 0 and ai_settings.bombs == True: # teste
        # Esvazia grupos
        aliens.empty()
        shots.empty()
        shots_aliens.empty()
        ai_settings.increase_speed()
        stats.level += 1 # Aumenta o level
        table_of_points.prep_level()
        ai_settings.alien_speed_factor = ai_settings.alien_speed_in_stage_game 
        ai_settings.bombs = False # teste
        create_fleet(ai_settings, screen, stats, ship, aliens)
        

def aliens_update(ai_settings, stats, screen, ship, aliens, shots, table_of_points, shots_aliens):
    check_alien_quantity(ai_settings, screen, stats, ship, aliens, shots, table_of_points, shots_aliens) 
    check_fleet_sides(ai_settings, aliens)
    # check_bomb(ai_settings, bombs)
    # Verifica se houve colisão com a ship
    if pygame.sprite.spritecollideany(ship, aliens): 
        collide_ship(ai_settings, screen, stats, ship, aliens, shots, table_of_points, shots_aliens)
    check_screen_botton(ai_settings, screen, stats, ship, aliens, shots, table_of_points, shots_aliens)
