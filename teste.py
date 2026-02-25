import pygame
import random

# Inicialização
pygame.init()

# Tela
LARGURA = 800
ALTURA = 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Jogo da Cobrinha 🐍")

# Cores
PRETO = (0, 0, 0)
VERDE = (0, 200, 0)
VERDE_CLARO = (0, 255, 0)
VERMELHO = (200, 0, 0)
BRANCO = (255, 255, 255)

# Relógio
clock = pygame.time.Clock()
velocidade = 15

# Fonte
fonte = pygame.font.SysFont("arial", 28)

# Função para mostrar pontuação
def mostrar_pontuacao(pontos):
    texto = fonte.render(f"Pontos: {pontos}", True, BRANCO)
    tela.blit(texto, (10, 10))

# Função para desenhar a cobrinha
def desenhar_cobra(tamanho, pixels):
    for pixel in pixels:
        pygame.draw.rect(tela, VERDE_CLARO, [pixel[0], pixel[1], tamanho, tamanho])

# Função principal
def jogo():
    fim = False
    x = LARGURA // 2
    y = ALTURA // 2
    dx = 0
    dy = 0

    tamanho_pixel = 20
    cobra = []
    comprimento = 1

    pontos = 0

    # Criar várias bolinhas
    comidas = []
    for _ in range(5):
        comidas.append([
            random.randrange(0, LARGURA - tamanho_pixel, 20),
            random.randrange(0, ALTURA - tamanho_pixel, 20)
        ])

    while not fim:
        tela.fill(PRETO)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                fim = True

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_LEFT:
                    dx = -tamanho_pixel
                    dy = 0
                elif evento.key == pygame.K_RIGHT:
                    dx = tamanho_pixel
                    dy = 0
                elif evento.key == pygame.K_UP:
                    dy = -tamanho_pixel
                    dx = 0
                elif evento.key == pygame.K_DOWN:
                    dy = tamanho_pixel
                    dx = 0

        x += dx
        y += dy

        # Bateu na parede
        if x < 0 or x >= LARGURA or y < 0 or y >= ALTURA:
            fim = True

        cabeca = [x, y]
        cobra.append(cabeca)

        if len(cobra) > comprimento:
            del cobra[0]

        # Bateu no próprio corpo
        for parte in cobra[:-1]:
            if parte == cabeca:
                fim = True

        # Desenhar comidas
        for comida in comidas:
            pygame.draw.circle(
                tela,
                VERMELHO,
                (comida[0] + 10, comida[1] + 10),
                8
            )

        # Comer comida
        for comida in comidas:
            if x == comida[0] and y == comida[1]:
                comida[0] = random.randrange(0, LARGURA - tamanho_pixel, 20)
                comida[1] = random.randrange(0, ALTURA - tamanho_pixel, 20)
                comprimento += 1
                pontos += 1

        desenhar_cobra(tamanho_pixel, cobra)
        mostrar_pontuacao(pontos)

        pygame.display.update()
        clock.tick(velocidade)

    pygame.quit()

# Executar jogo
jogo()