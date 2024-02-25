import json
import time


class GameStats:
# Armazena dados sobre o jogo
    def __init__(self, ai_settings):
        self.ai_settings = ai_settings
        self.resetar_status()
        self.game_active = False
        self.level = ai_settings.level
        self.score = 0
        self.bullet_shots = 0
        self.alienigenas_mortos = 0
        self.tempo = time.time()

    def resetar_status(self):
        self.ships_left = self.ai_settings.ship_limit
        self.level = 1
        self.score = 0
        self.bullet_shots = 0
        self.alienigenas_mortos = 0

        arquivo_json = open('tabela.json')
        tabela_json = json.load(arquivo_json)
        self.high_score = tabela_json['pontuacao_maxima']

    def registrar_tabela_json(self):
        # faz parte de registrar_tabela_json
        with open('tabela.json') as arquivo_json:
            tabela_json = json.load(arquivo_json)
            tabela_json['numero_testes'] += 1
            if self.score > tabela_json['pontuacao_maxima']: 
                tabela_json['pontuacao_maxima'] = self.score
            tabela_json = json.dumps(tabela_json, indent=4)
        arquivo_json = open('tabela.json', 'wt')
        arquivo_json.write(tabela_json)
        arquivo_json.close()

    def registrar_partida(self):
        # faz parte de registrar_tabela_json
        with open('tabela.json') as arquivo_json:
            tabela_json = json.load(arquivo_json)
            numero_teste = tabela_json['numero_testes']
            arquivo_json.close()
        level = self.level
        pontuacao_alcancada = self.score 
        aliens_mortos = self.alienigenas_mortos
        tiros_disparados = self.bullet_shots
        texto_registro = ''
        texto_registro += '----------------------------------------\n'
        texto_registro += f'Numero do teste: {numero_teste}\nNivel: {level}\nPontuacao alcancada: {pontuacao_alcancada}\n'
        texto_registro += f'Alienigenas mortos: {aliens_mortos}\nTiros disparados: {tiros_disparados}\n'
        texto_registro += '----------------------------------------\n'
        with open('registros.txt', 'at') as registros_txt:
            registros_txt.write(texto_registro)
            registros_txt.close()

    # aaaaaaaaaaaaaaaaaaaaaaaaaaaahhhhhhhhh
    def iniciar_cronometro(self):
        with open('tabela.json') as arquivo_json:
            tabela_json = json.load(arquivo_json)
            tabela_json['tempo'] = float(self.tempo)
            tabela_json = json.dumps(tabela_json, indent=4)
        arquivo_json = open('tabela.json', 'wt')
        arquivo_json.write(tabela_json)
        arquivo_json.close()

    def cronometro(self):
        with open('tabela.json') as arquivo_json:
            tabela_json = json.load(arquivo_json)
            print(str(self.tempo) +' - '+ str(tabela_json['tempo']))
            # print(self.tempo - tabela_json['tempo'])
            arquivo_json.close()

