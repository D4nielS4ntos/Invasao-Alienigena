import json
from random import choice
from operator import itemgetter

class GameStats:
# Armazena dados sobre o jogo
    def __init__(self, ai_settings):
        self.ai_settings = ai_settings
        self.level = ai_settings.level
        self.game_active = False
        self.score = 0
        self.bullet_shots = 0
        self.alien_deaths = 0
        self.name = 'digite seu nome...'
        self.initial_time = 0
        self.current_time = 0
        self.time_of_question_set = 0
        self.reset_stats()

    def reset_stats(self):
        self.ships_left = self.ai_settings.ship_limit
        self.level = self.ai_settings.level
        self.score = 0
        self.bullet_shots = 0
        self.alien_deaths = 0
        self.alien_deaths = 0
        self.initial_time = 0
        self.current_time = 0
        self.time_of_question_set = 0

        json_arquive = open('tabela.json')
        self.json_table = json.load(json_arquive)
        self.high_score_name = self.json_table['placar'][-1]['pontuacao_maxima_nome']
        self.second_high_score_name = self.json_table['placar'][-2]['pontuacao_maxima_nome']
        self.third_high_score_name = self.json_table['placar'][-3]['pontuacao_maxima_nome']

        self.high_score = self.json_table['placar'][-1]['pontuacao_maxima']
        self.second_high_score = self.json_table['placar'][-2]['pontuacao_maxima']
        self.third_high_score = self.json_table['placar'][-3]['pontuacao_maxima']
        
        self.reset_questions()

    def reset_questions(self):
        json_questions_arquive = open('perguntas.json')
        self.json_questions_table = json.load(json_questions_arquive)
        self.number_of_questions = len(self.json_questions_table['perguntas'])
        self.list_numbers_of_questions = list(range(self.number_of_questions))
        self.current_question = choice(self.list_numbers_of_questions)

    def register_json_table(self):
        # faz parte de register_json_table
        result = {
            'pontuacao_maxima': self.score,
            'pontuacao_maxima_nome': self.name.upper()
        }
        with open('tabela.json') as json_arquive:
            json_table = json.load(json_arquive)
            json_table['numero_testes'] += 1
            json_table['placar'].append(result)
            json_table['placar'].sort(key=itemgetter('pontuacao_maxima'))
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
        name = self.name.upper()
        level = self.level
        score_achived = self.score 
        alien_deaths = self.alien_deaths
        bullet_shots = self.bullet_shots
        time_playing = round(self.current_time - self.initial_time, 2)
        texto_registro = ''
        texto_registro += '----------------------------------------\n'
        texto_registro += f'Numero do teste: {test_number}\nNome: {name}\nNivel: {level}\nPontuacao alcancada: {score_achived}\n'
        texto_registro += f'Alienigenas mortos: {alien_deaths}\nTiros disparados: {bullet_shots}\nTempo gasto {time_playing}\n'
        texto_registro += '----------------------------------------\n'
        with open('registros.txt', 'at') as registros_txt:
            registros_txt.write(texto_registro)
            registros_txt.close()
