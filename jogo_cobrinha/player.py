#Aqui fica a cobra

import pygame

class Cobra:
    def __init__(self, x, y, velocidade):
        self.x = x
        self.y = y
        self.velocidade = velocidade
        self.lista = []
        self.comprimento = 5

    def mover(self, dx, dy):
        self.x += dx
        self.y += dy
        self.lista.append([self.x, self.y])

        if len(self.lista) > self.comprimento:
            del self.lista[0]

    def desenhar(self, tela):
        for x, y in self.lista:
            pygame.draw.circle(tela, (0,200,100), (x,y), 10)