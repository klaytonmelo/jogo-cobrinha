'''
Aqui fica a “inteligência” do jogo:
estados (menu, jogando, game over), níveis, regras
'''
import pygame
from config import *

MENU = "menu"
JOGANDO = "jogando"
GAME_OVER = "game_over"
LEVEL_UP = "level_up"

class Game:
    def __init__(self):
        self.estado = MENU
        self.nivel = 1
        self.pontos = 0

    def iniciar_nivel(self, config):
        self.pontos = 0
        self.estado = JOGANDO