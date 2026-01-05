import pygame
from pygame.locals import *
from sys import exit
from random import randint
import math

MENU = "menu"
JOGANDO = "jogando"
LEVEL_UP = "level_up"

PONTOS_PARA_PROX_NIVEL = 5

estado = JOGANDO
nivel = 1

pygame.init()

# Música
pygame.mixer.music.set_volume(0.05)
pygame.mixer.music.load('musica_jogo.mp3')
pygame.mixer.music.play(-1)

colisao = pygame.mixer.Sound('musica_da_comida.wav')

# Tela
largura = 1000
altura = 700
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption('Jogo da Cobra')

relogio = pygame.time.Clock()

# Cobra
x_cobra = largura // 2
y_cobra = altura // 2
velocidade = 5
x_controle = velocidade
y_controle = 0

lista_cobra = []
comprimento_inicial = 5

# Maçã
x_maca = randint(40, 960)
y_maca = randint(40, 660)

# Pontos
pontos = 0
font = pygame.font.SysFont("gabriola", 38, True, True)

morreu = False

# Funções 

#corpo dacobra
def aumenta_cobra(lista_cobra):
    for XeY in lista_cobra[:-1]:
        pygame.draw.circle(tela, (0, 200, 100), (XeY[0], XeY[1]), 12)

def reiniciar_jogo():
    global pontos, comprimento_inicial, x_cobra, y_cobra, lista_cobra, x_maca, y_maca, morreu
    pontos = 0
    comprimento_inicial = 5
    x_cobra = largura // 2
    y_cobra = altura // 2
    lista_cobra = []
    x_maca = randint(40, 960)
    y_maca = randint(40, 660)
    morreu = False

#tela pra proximo level   
def tela_level_up(nivel):
    tela.fill((0, 0, 0))
    fonte = pygame.font.SysFont('arial', 48, True)
    fonte2 = pygame.font.SysFont('arial', 28, True)

    texto = fonte.render(f"NÍVEL {nivel} CONCLUÍDO!", True, (255, 255, 0))
    instrucao = fonte2.render("Pressione ENTER para o próximo nível", True, (255, 255, 255))

    tela.blit(texto, (largura//2 - texto.get_width()//2, 250))
    tela.blit(instrucao, (largura//2 - instrucao.get_width()//2, 320))

def iniciar_nivel(nivel):
    global x_cobra, y_cobra, lista_cobra, comprimento_inicial
    global x_controle, y_controle, velocidade

    x_cobra = largura // 2
    y_cobra = altura // 2
    lista_cobra = []
    comprimento_inicial = 5

    x_controle = velocidade
    y_controle = 0

    if nivel == 1:
        velocidade = 5
    elif nivel == 2:
        velocidade = 8
    elif nivel == 3:
        velocidade = 11

# Loop principal
while True:
    relogio.tick(40)
    tela.fill((0, 0, 0))
    if estado == JOGANDO:
        texto_pontos = font.render(f"Pontos: {pontos}", True, (255, 255, 255))
        tela.blit(texto_pontos, (420, 40))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()

        if estado == JOGANDO:
            if event.type == KEYDOWN:
                if event.key == K_a and x_controle != velocidade:
                    x_controle = -velocidade
                    y_controle = 0
                elif event.key == K_d and x_controle != -velocidade:
                    x_controle = velocidade
                    y_controle = 0
                elif event.key == K_w and y_controle != velocidade:
                    y_controle = -velocidade
                    x_controle = 0
                elif event.key == K_s and y_controle != -velocidade:
                    y_controle = velocidade
                    x_controle = 0
        #Tela de level up
        elif estado == LEVEL_UP:

            if event.type == KEYDOWN and event.key == K_RETURN:
                nivel += 1
                pontos = 0
                iniciar_nivel(nivel)
                estado = JOGANDO

    # Movimento
    if estado == JOGANDO:
        x_cobra += x_controle
        y_cobra += y_controle

    

    # Desenhos
    # Desenha o corpo primeiro
    if estado == JOGANDO:
        aumenta_cobra(lista_cobra)
        #cobra = pygame.draw.rect(tela, (0, 255, 0), (x_cobra, y_cobra, 40,40))
        cobra = pygame.draw.circle(tela,(50, 100, 144),(x_cobra, y_cobra),13)
        maca = pygame.draw.circle(tela, (255, 0, 0), (x_maca, y_maca), 10)

        # Colisão com maçã
        if cobra.colliderect(maca):
            x_maca = randint(40, 960)
            y_maca = randint(40, 660)
            pontos += 1
            if pontos == PONTOS_PARA_PROX_NIVEL:
                estado = LEVEL_UP

            colisao.play()
            comprimento_inicial += 5

    # Corpo da cobra
    if estado == JOGANDO:
        lista_cabeca = [x_cobra, y_cobra]
        lista_cobra.append(lista_cabeca)

    #quando a cobra morre
    if lista_cobra.count(lista_cabeca) > 1:
        font2 = pygame.font.SysFont('arial', 24, True, True)
        mensagem = "GAME OVER - Pressione R para jogar novamente"
        texto = font2.render(mensagem, True, (255, 255, 255))
        rect = texto.get_rect(center=(largura // 2, altura // 2))
        

        morreu = True
        while morreu:
            tela.fill((200, 50, 50))
            tela.blit(texto, rect)
            pygame.mixer.music.play(0)

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()
                if event.type == KEYDOWN and event.key == K_r:
                    reiniciar_jogo()

            pygame.display.update()

    if len(lista_cobra) > comprimento_inicial:
        del lista_cobra[0]

    # Teleporte nas bordas
    if x_cobra >= largura:
        x_cobra = 0
    elif x_cobra <= 0:
        x_cobra = largura
    elif y_cobra >= altura:
        y_cobra = 10
    elif y_cobra < 10:
        y_cobra = altura

    if estado == LEVEL_UP:
        tela_level_up(nivel)

    pygame.display.update()
