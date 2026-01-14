import pygame
from pygame.locals import *
from sys import exit
from random import randint

pygame.init()

#musica
pygame.mixer.music.set_volume(0.05)
pygame.mixer.music.load("musica_jogo.mp3")
pygame.mixer.music.play(-1)

m_colisao = pygame.mixer.Sound("musica_da_comida.wav")
#CONFIGURAÇÕES

NIVEIS = {
    1: {
        "velocidade": 5,
        "objetivo": "pontos",
        "valor_objetivo": 2,
        "obstaculos": [],
        "tempo_limite": None
    },
    2: {
        "velocidade": 7,
        "objetivo": "pontos",
        "valor_objetivo": 3,
        "obstaculos": [pygame.Rect(300, 200, 40, 40)],
        "tempo_limite": None
    },
    3: {
        "velocidade": 5,
        "objetivo": "tempo",
        "valor_objetivo": 10,
        "obstaculos": [
            pygame.Rect(200, 300, 40, 40),
            pygame.Rect(600, 300, 40, 40)
        ],
        "tempo_limite": 10
    },
    4: {
        "velocidade": 5,
        "objetivo": "pontos_tempo",
        "valor_objetivo": 5,
        "obstaculos": [
            pygame.Rect(200, 300, 40, 40),
            pygame.Rect(600, 300, 40, 40)
        ],
        "tempo_limite": 10
    }
}

MENU = "menu"
JOGANDO = "jogando"
LEVEL_UP = "level_up"
GAME_OVER = "game_over"

# ================= VARIÁVEIS =================

largura = 1000
altura = 700
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Jogo da Cobra")

relogio = pygame.time.Clock()
font = pygame.font.SysFont("gabriola", 36, True)

estado = JOGANDO
nivel = 1

x_cobra = largura // 2
y_cobra = altura // 2
velocidade = 5
x_controle = velocidade
y_controle = 0

lista_cobra = []
comprimento_inicial = 5

x_maca = randint(40, 960)
y_maca = randint(40, 660)

pontos = 0
objetivo = None
valor_objetivo = 0
tempo_limite = None
obstaculos = []
tempo_inicio = 0

# ================= FUNÇÕES =================

def aumenta_cobra(lista):
    for x, y in lista[:-1]:
        pygame.draw.circle(tela, (0, 200, 100), (x, y), 12)

def tela_game_over():
    tela.fill((120, 0, 0))
    texto = pygame.font.SysFont("arial", 50, True).render("GAME OVER", True, (255,255,255))
    instrucao = pygame.font.SysFont("arial", 26).render("Pressione R para reiniciar", True, (255,255,255))
    tela.blit(texto, (largura//2 - texto.get_width()//2, 260))
    tela.blit(instrucao, (largura//2 - instrucao.get_width()//2, 330))

def tela_level_up(n):
    tela.fill((0,0,0))
    texto = pygame.font.SysFont("arial", 50, True).render(f"NÍVEL {n} CONCLUÍDO!", True, (255,255,0))
    instrucao = pygame.font.SysFont("arial", 26).render("Pressione ENTER", True, (255,255,255))
    tela.blit(texto, (largura//2 - texto.get_width()//2, 260))
    tela.blit(instrucao, (largura//2 - instrucao.get_width()//2, 330))
    pygame.mixer.music.pause()

def iniciar_nivel(n):
    global velocidade, objetivo, valor_objetivo, obstaculos, tempo_inicio
    global x_cobra, y_cobra, lista_cobra, comprimento_inicial
    global x_controle, y_controle, tempo_limite, pontos

    config = NIVEIS[n]

    velocidade = config["velocidade"]
    objetivo = config["objetivo"]
    valor_objetivo = config["valor_objetivo"]
    obstaculos = config["obstaculos"]
    tempo_limite = config["tempo_limite"]

    pontos = 0
    tempo_inicio = pygame.time.get_ticks()

    x_cobra = largura // 2
    y_cobra = altura // 2
    lista_cobra = []
    comprimento_inicial = 5

    x_controle = velocidade
    y_controle = 0
    pygame.mixer.music.play(-1)

def verificar_objetivo():
    global estado
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

def desenhar_obstaculos(cobra):
    for obs in obstaculos:
        pygame.draw.rect(tela, (255,0,0), obs)
        if cobra.colliderect(obs):
            return True
    return False

# ================= INÍCIO =================

iniciar_nivel(nivel)

# ================= LOOP PRINCIPAL =================

while True:
    relogio.tick(40)
    tela.fill((0,0,0))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()

        if estado == JOGANDO and event.type == KEYDOWN:
            if event.key == K_a and x_controle != velocidade:
                x_controle = -velocidade; y_controle = 0
            elif event.key == K_d and x_controle != -velocidade:
                x_controle = velocidade; y_controle = 0
            elif event.key == K_w and y_controle != velocidade:
                y_controle = -velocidade; x_controle = 0
            elif event.key == K_s and y_controle != -velocidade:
                y_controle = velocidade; x_controle = 0

        if estado == GAME_OVER and event.type == KEYDOWN and event.key == K_r:
            nivel = 1
            estado = JOGANDO
            iniciar_nivel(nivel)

        if estado == LEVEL_UP and event.type == KEYDOWN and event.key == K_RETURN:
            nivel += 1
            if nivel in NIVEIS:
                estado = JOGANDO
                iniciar_nivel(nivel)
            else:
                pygame.quit()
                exit()

    if estado == JOGANDO:
        x_cobra += x_controle
        y_cobra += y_controle

        lista_cobra.append([x_cobra, y_cobra])
        if len(lista_cobra) > comprimento_inicial:
            del lista_cobra[0]

        aumenta_cobra(lista_cobra)
        cobra = pygame.draw.circle(tela, (50,100,144), (x_cobra, y_cobra), 13)
        maca = pygame.draw.circle(tela, (255,0,0), (x_maca, y_maca), 10)

        if cobra.colliderect(maca):
            x_maca = randint(40, 960)
            y_maca = randint(40, 660)
            pontos += 1
            m_colisao.play()
            comprimento_inicial += 5

        if desenhar_obstaculos(cobra):
            estado = GAME_OVER

        if lista_cobra.count([x_cobra, y_cobra]) > 1:
            estado = GAME_OVER

        if x_cobra < 0 or x_cobra > largura or y_cobra < 0 or y_cobra > altura:
            estado = GAME_OVER

        verificar_objetivo()

        tempo_passado = (pygame.time.get_ticks() - tempo_inicio) // 1000
        if tempo_limite:
            tempo_restante = max(0, tempo_limite - tempo_passado)
            tela.blit(font.render(f"Tempo: {tempo_restante}s", True, (255,255,255)), (40,40))

        tela.blit(font.render(f"Pontos: {pontos}", True, (255,255,255)), (420,40))

        if objetivo == "pontos_tempo":
            tela.blit(
                font.render(f"Objetivo: {valor_objetivo} pontos em {tempo_limite}s", True, (255,255,0)),
                (300,80)
            )

    elif estado == GAME_OVER:
        tela_game_over()

    elif estado == LEVEL_UP:
        tela_level_up(nivel)

    pygame.display.update()

