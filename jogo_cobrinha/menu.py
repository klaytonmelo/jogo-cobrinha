#menu do jogo

import pygame

def desenhar_menu(tela, largura, altura, font):
    tela.fill((0,0,0))

    titulo = font.render("JOGO DA COBRA", True, (0,255,0))
    jogar = font.render("ENTER para jogar", True, (255,255,255))

    tela.blit(titulo, (largura//2 - titulo.get_width()//2, 200))
    tela.blit(jogar, (largura//2 - jogar.get_width()//2, 350))