import sys
import os
import time
from time import sleep
from random import randint, choice
import json
from operator import itemgetter

import cx_Freeze
import pygame
from pygame.sprite import Sprite


def find_data_file(filename):
    if getattr(sys, "frozen", False):
        # The application is frozen
        datadir = os.path.dirname(sys.executable)
    else:
        # The application is not frozen
        # Change this bit to match where you store your data files:
        datadir = os.path.dirname(__file__)
    return os.path.join(datadir, filename)


executables = [cx_Freeze.Executable('main.py')]

cx_Freeze.setup(
    name="TCC",
    options={'build_exe': {'packages':['pygame'],
                           'include_files':['classes', 'imagens', 'sons', find_data_file('perguntas.json'), find_data_file('tabela.json'), find_data_file('registros.txt')]}
                           },

    executables = executables
    
)