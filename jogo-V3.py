import pygame
from pygame.locals import *
from sys import exit
from random import randint
import math

NIVEIS = {
    1: {
        "velocidade": 5,
        "objetivo": "pontos",
        "valor_objetivo": 2,
        "valor_objetivo2": 0,
        "obstaculos": [],
        "tempo_limite": None
    },
    2: {
        "velocidade": 7,
        "objetivo": "pontos",
        "valor_objetivo": 3,
        "obstaculos": [
            pygame.Rect(300, 200, 40, 40)
        ],
        "tempo_limite": None
    },
    3: {
        "velocidade": 5,
        "objetivo": "tempo",
        "valor_objetivo": 10,  # sobreviver 20s
        "obstaculos": [
            pygame.Rect(200, 300, 40, 40),
            pygame.Rect(600, 300, 40, 40),
            pygame.Rect(300, 400, 40, 40),
            pygame.Rect(100, 150, 40, 100)
        ],
        "tempo_limite": 20
    },
    4: {
        "velocidade": 5,
        "objetivo": "pontos_tempo",
        "valor_objetivo": 20,  # sobreviver 20s
        "obstaculos": [
            pygame.Rect(200, 300, 40, 40),
            pygame.Rect(600, 300, 40, 40)
        ],
        "tempo_limite": 20
    }
    
}

MENU = "menu"
JOGANDO = "jogando"
LEVEL_UP = "level_up"
GAME_OVER = "game_over"

PONTOS_PARA_PROX_NIVEL = 5

tempo_limite = None


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


objetivo = None
valor_objetivo = 0
obstaculos = []
tempo_inicio = 0

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

#tela GAME OVER
def tela_game_over():
    tela.fill((120, 0, 0))
    fonte = pygame.font.SysFont('arial', 48, True)
    fonte2 = pygame.font.SysFont('arial', 26)

    texto = fonte.render("GAME OVER", True, (255, 255, 255))
    instrucao = fonte2.render("Pressione R para reiniciar", True, (255, 255, 255))

    tela.blit(texto, (largura//2 - texto.get_width()//2, 260))
    tela.blit(instrucao, (largura//2 - instrucao.get_width()//2, 320))

#função para iniciar qualquer nivel
def iniciar_nivel(nivel):
    global velocidade, objetivo, valor_objetivo, obstaculos, tempo_inicio
    global x_cobra, y_cobra, lista_cobra, comprimento_inicial
    global x_controle, y_controle
    global tempo_limite

    config = NIVEIS[nivel]

    tempo_limite = config["tempo_limite"]
    velocidade = config["velocidade"]
    objetivo = config["objetivo"]
    valor_objetivo = config["valor_objetivo"]
    obstaculos = config["obstaculos"]

    tempo_inicio = pygame.time.get_ticks()

    x_cobra = largura // 2
    y_cobra = altura // 2
    lista_cobra = []
    comprimento_inicial = 5

    x_controle = velocidade
    y_controle = 0

#sistema de objetivo
def verificar_objetivo():
    global estado, nivel

    tempo_passado = (pygame.time.get_ticks() - tempo_inicio) // 1000

    if objetivo == "pontos":
        if pontos >= valor_objetivo:
            estado = LEVEL_UP

    elif objetivo == "tempo":
        if tempo_passado >= valor_objetivo:
            estado = LEVEL_UP

    elif objetivo == "pontos_tempo":
        if pontos >= valor_objetivo:
            estado = LEVEL_UP
        elif tempo_passado >= tempo_limite:
            estado = GAME_OVER
        

#obstaculo por nivel
def desenhar_obstaculos():
    global estado
    for obs in obstaculos:
        pygame.draw.rect(tela, (255, 0, 0), obs)
        if cobra.colliderect(obs):
            estado = GAME_OVER

#tela do jogo
'''def tela_jogo():
    pass'''

iniciar_nivel(nivel)

# Loop principal
while True:
    relogio.tick(40)
    tela.fill((0, 0, 0))
    if estado == JOGANDO:
        texto_pontos = font.render(f"Pontos: {pontos}", True, (255, 255, 255))
        tela.blit(texto_pontos, (420, 40))

        if objetivo in ("tempo", "pontos_tempo"):
            tempo_passado = (pygame.time.get_ticks() - tempo_inicio) // 1000
            tempo_restante = tempo_limite - tempo_passado if tempo_limite else tempo_passado

            texto_tempo = font.render(f"Tempo: {tempo_restante}s", True, (255, 255, 255))
            tela.blit(texto_tempo, (40, 40))

    #bloco de eventos
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

                #tela_jogo()

        elif estado == GAME_OVER:
            if event.type == KEYDOWN and event.key == K_r:
                nivel = 1
                pontos = 0
                iniciar_nivel(nivel)
                estado = JOGANDO
        #Tela de level up
        elif estado == LEVEL_UP:

            if event.type == KEYDOWN and event.key == K_RETURN:
                nivel += 1
                pontos = 0
                if nivel in NIVEIS:
                    iniciar_nivel(nivel)
                    estado = JOGANDO
                else:
                    print("JOGO ZERADO!")  # depois você pode criar uma tela
                    estado = MENU
                    
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
        desenhar_obstaculos()

        # Colisão com maçã
        if cobra.colliderect(maca):
            x_maca = randint(40, 960)
            y_maca = randint(40, 660)
            pontos += 1

            colisao.play()
            comprimento_inicial += 5

    # Corpo da cobra
    if estado == JOGANDO:
        lista_cabeca = [x_cobra, y_cobra]
        lista_cobra.append(lista_cabeca)

    #quando a cobra morre
    if estado == JOGANDO and lista_cobra.count(lista_cabeca) > 1:
        estado = GAME_OVER

    if len(lista_cobra) > comprimento_inicial:
        del lista_cobra[0]
    
    #verifica o objetivo do jogo
    if estado == JOGANDO:
        verificar_objetivo()


    # Teleporte nas bordas
    '''if x_cobra >= largura:
        x_cobra = 0
    elif x_cobra <= 0:
        x_cobra = largura
    elif y_cobra >= altura:
        y_cobra = 10
    elif y_cobra < 10:
        y_cobra = altura'''
    
    #morte nas bordas
    if x_cobra > largura or x_cobra < 0:
        tela_game_over()
        estado = GAME_OVER
    elif y_cobra > altura or y_cobra < 10:
        tela_game_over()
        estado = GAME_OVER

    if estado == LEVEL_UP:
        tela_level_up(nivel)
    elif estado == GAME_OVER:
        tela_game_over()


    pygame.display.update()
