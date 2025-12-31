import pygame
from pygame.locals import *
from sys import exit
from random import randint
import math

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
def aumenta_cobra(lista_cobra):
    for XeY in lista_cobra[:-1]:
        pygame.draw.circle(tela, (0, 200, 100), (XeY[0], XeY[1]), 17)

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

'''def colidiu_com_corpo(x, y, corpo):
    for parte in corpo[:-1]:  # ignora a cabeça
        distancia = math.sqrt((x - parte[0])**2 + (y - parte[1])**2)
        if distancia < 18 + 17:  # raio cabeça + raio corpo
            return True
    return False'''

# Loop principal
while True:
    relogio.tick(40)
    tela.fill((0, 0, 0))

    texto_pontos = font.render(f"Pontos: {pontos}", True, (255, 255, 255))
    tela.blit(texto_pontos, (420, 40))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()

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

    # Movimento
    x_cobra += x_controle
    y_cobra += y_controle

    # Desenhos
    # Desenha o corpo primeiro
    aumenta_cobra(lista_cobra)
    #cobra = pygame.draw.rect(tela, (0, 255, 0), (x_cobra, y_cobra, 40,40))
    cobra = pygame.draw.circle(tela,(50, 100, 144),(x_cobra, y_cobra),18)
    maca = pygame.draw.circle(tela, (255, 0, 0), (x_maca, y_maca), 20)

    # Colisão com maçã
    if cobra.colliderect(maca):
        x_maca = randint(40, 960)
        y_maca = randint(40, 660)
        pontos += 1
        colisao.play()
        comprimento_inicial += 5

    # Corpo da cobra
    lista_cabeca = [x_cobra, y_cobra]
    lista_cobra.append(lista_cabeca)

    if lista_cobra.count(lista_cabeca) > 1:
        font2 = pygame.font.SysFont('arial', 24, True, True)
        mensagem = "GAME OVER - Pressione R para jogar novamente"
        texto = font2.render(mensagem, True, (255, 255, 255))
        rect = texto.get_rect(center=(largura // 2, altura // 2))

        morreu = True
        while morreu:
            tela.fill((200, 50, 50))
            tela.blit(texto, rect)

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
    if x_cobra > largura:
        x_cobra = 0
    elif x_cobra < 0:
        x_cobra = largura
    elif y_cobra > altura:
        y_cobra = 0
    elif y_cobra < 0:
        y_cobra = altura

    pygame.display.update()
