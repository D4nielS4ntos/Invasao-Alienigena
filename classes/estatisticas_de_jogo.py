import json
# import time


class GameStats:
# Armazena dados sobre o jogo
    def __init__(self, ai_settings):
        self.ai_settings = ai_settings
        self.reset_stats()
        self.game_active = False
        self.level = ai_settings.level
        self.score = 0
        self.bullet_shots = 0
        self.alien_deaths = 0
        # self.time = time.time()

    def reset_stats(self):
        self.ships_left = self.ai_settings.ship_limit
        self.level = 1
        self.score = 0
        self.bullet_shots = 0
        self.alien_deaths = 0

        json_arquive = open('tabela.json')
        json_table = json.load(json_arquive)
        self.high_score = json_table['pontuacao_maxima']

    def register_json_table(self):
        # faz parte de register_json_table
        with open('tabela.json') as json_arquive:
            json_table = json.load(json_arquive)
            json_table['numero_testes'] += 1
            if self.score > json_table['pontuacao_maxima']: 
                json_table['pontuacao_maxima'] = self.score
            json_table = json.dumps(json_table, indent=4)
        json_arquive = open('tabela.json', 'wt')
        json_arquive.write(json_table)
        json_arquive.close()

    def play_register(self):
        # faz parte de register_json_table
        with open('tabela.json') as json_arquive:
            json_table = json.load(json_arquive)
            test_number = json_table['numero_testes']
            json_arquive.close()
        level = self.level
        score_achived = self.score 
        alien_deaths = self.alien_deaths
        bullet_shots = self.bullet_shots
        texto_registro = ''
        texto_registro += '----------------------------------------\n'
        texto_registro += f'Numero do teste: {test_number}\nNivel: {level}\nPontuacao alcancada: {score_achived}\n'
        texto_registro += f'Alienigenas mortos: {alien_deaths}\nTiros disparados: {bullet_shots}\n'
        texto_registro += '----------------------------------------\n'
        with open('registros.txt', 'at') as registros_txt:
            registros_txt.write(texto_registro)
            registros_txt.close()

    # aaaaaaaaaaaaaaaaaaaaaaaaaaaahhhhhhhhh
    # def iniciar_cronometro(self):
    #     with open('tabela.json') as json_arquive:
    #         json_table = json.load(json_arquive)
    #         json_table['tempo'] = float(self.tempo)
    #         json_table = json.dumps(json_table, indent=4)
    #     json_arquive = open('tabela.json', 'wt')
    #     json_arquive.write(json_table)
    #     json_arquive.close()

    # def cronometro(self):
    #     with open('tabela.json') as json_arquive:
    #         json_table = json.load(json_arquive)
    #         print(str(self.tempo) +' - '+ str(json_table['tempo']))
    #         # print(self.tempo - json_table['tempo'])
    #         json_arquive.close()
