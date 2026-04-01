# loop principal

import pygame
from config import *
from game import Game, MENU, JOGANDO, GAME_OVER, LEVEL_UP
from menu import desenhar_menu
from random import randint

pygame.init()

tela = pygame.display.set_mode((LARGURA, ALTURA))
clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 30)

game = Game()

# variáveis do jogo (devem existir aqui ou vir de outra classe depois)
x_cobra = LARGURA // 2
y_cobra = ALTURA // 2
x_controle = 5
y_controle = 0

lista_cobra = []
comprimento_inicial = 5

x_maca = randint(40, 960)
y_maca = randint(40, 660)

pontos = 0
tempo_inicio = pygame.time.get_ticks()

obstaculos = []
tempo_limite = None
objetivo = None
valor_objetivo = 0

while True:
    clock.tick(FPS)

    # ================= EVENTOS =================
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        
        if game.estado == MENU:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                game.estado = JOGANDO

        elif game.estado == GAME_OVER:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                game = Game()
                x_cobra = LARGURA // 2
                y_cobra = ALTURA // 2
                lista_cobra = []
                pontos = 0
                tempo_inicio = pygame.time.get_ticks()

        elif game.estado == LEVEL_UP:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                game.nivel += 1
                game.estado = JOGANDO

        # controle da cobra
        elif game.estado == JOGANDO:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    x_controle = -5
                    y_controle = 0
                elif event.key == pygame.K_d:
                    x_controle = 5
                    y_controle = 0
                elif event.key == pygame.K_w:
                    y_controle = -5
                    x_controle = 0
                elif event.key == pygame.K_s:
                    y_controle = 5
                    x_controle = 0
    
    # ================= RENDER =================
    if game.estado == MENU:
        desenhar_menu(tela, LARGURA, ALTURA, font)

    elif game.estado == JOGANDO:
        tela.fill((0,0,0))

        # movimento
        x_cobra += x_controle
        y_cobra += y_controle

        lista_cobra.append([x_cobra, y_cobra])

        if len(lista_cobra) > comprimento_inicial:
            del lista_cobra[0]

        # desenhar cobra
        for segmento in lista_cobra[:-1]:
            pygame.draw.circle(tela, (0,200,100), segmento, 12)

        cobra = pygame.draw.circle(tela, (50,100,144), (x_cobra, y_cobra), 13)

        # maçã
        maca = pygame.draw.circle(tela, (255,0,0), (x_maca, y_maca), 10)

        # colisão maçã
        if cobra.colliderect(maca):
            x_maca = randint(40, 960)
            y_maca = randint(40, 660)
            pontos += 1
            comprimento_inicial += 5

        # colisão com parede
        if x_cobra < 0 or x_cobra > LARGURA or y_cobra < 0 or y_cobra > ALTURA:
            game.estado = GAME_OVER

        # colisão com si mesma
        if lista_cobra.count([x_cobra, y_cobra]) > 1:
            game.estado = GAME_OVER

        # tempo
        tempo_passado = (pygame.time.get_ticks() - tempo_inicio) // 1000

        tela.blit(font.render(f"Pontos: {pontos}", True, (255,255,255)), (420,40))

        pygame.display.update()

    elif game.estado == GAME_OVER:
        tela.fill((120,0,0))
        texto = font.render("GAME OVER - R para reiniciar", True, (255,255,255))
        tela.blit(texto, (200,300))

    elif game.estado == LEVEL_UP:
        tela.fill((0,0,0))
        texto = font.render("LEVEL UP - ENTER para continuar", True, (255,255,0))
        tela.blit(texto, (200,300))

    pygame.display.update()