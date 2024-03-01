class Config:
# Configurações do jogo
    def __init__(self):
    # Configurações da tela 
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (0, 0, 0) 
    # Configurações da nave
        self.ship_speed_factor = 1.5
        self.ship_limit = 3
    # Configurações do disparo
        self.bullet_speed_factor = 2
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (230, 230, 230) 
        self.bullets_allowed = 3
        self.disparando = False
        # teste
        self.alien_bullet_speed_factor = 1
        self.alien_bullet_width = 3
        self.alien_bullet_height = 15
        self.alien_bullet_color = (0, 255, 50) 
        self.alien_bullets_allowed = 3
    # Configurações da frota
        self.alien_speed_factor = 1
        self.alien_speed_in_stage_game = 1
        self.fleet_drop_speed = 10
        self.fleet_direction = 1
        self.alien_bomb_speed = 0.2
        self.alienigenas = False 
        self.alienigenas_bomba = False 
    # Configurações de aumentos do jogo
        self.speed_up_scale = 1.1
        self.score_scale = 1.5
        self.alien_points = 50
        self.level = 1
        self.initialize_dynamic_settings()
    # Configurações botão
        self.button_color = (0, 255, 0)
        self.text_color = (255, 255, 255)
    # Configurações tabela de pontos
        self.table_color = (200, 200, 0)

        
    def initialize_dynamic_settings(self): 
    # Configurações da nave
        self.ship_speed_factor = 1.5
    # Configurações do disparo
        self.bullet_width = 3 #*100
        self.bullet_height = 15
        self.bullet_color = (230, 230, 230)
        self.bullets_allowed = 3
        self.bullet_speed_factor = 2
    # Configurações da frota
        self.alien_speed_factor = 1
        self.alien_speed_in_stage_game = 1
        self.alien_speed_factor = 1
        self.alien_bomb_speed = 0.2 
    # Configurações de aumentos do jogo
        self.speed_up_scale = 1.1
        self.alien_points = 50
        

    def increase_speed(self): 
        # A velocidade para de aumentar a partir do level 10
        if self.level <= 10: 
            self.alien_speed_factor *= self.speed_up_scale
            self.alien_points = int(self.alien_points * self.score_scale)
            self.alien_speed_in_stage_game *= self.speed_up_scale # Velocidade que inicia o nível
            self.level += 1
