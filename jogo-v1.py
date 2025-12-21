import pygame
from pygame.locals import *
from sys import exit
from random import randint
#sorteia valores dentro de um intervalo

pygame.init()# inicia todos os recursos do pygame

pygame.mixer.music.set_volume(0.05)
pygame.mixer.music.load('musica_jogo.mp3')
pygame.mixer.music.play(-1)#musica de fundo

colisao = pygame.mixer.Sound('musica_da_comida.wav')

largura = 1000
altura = 700

x_cobra = int(largura / 2)
y_cobra = int(altura / 2)

velocidade = 5

x_controle = velocidade
y_controle = 0


x_maca = randint(40, 600)
y_maca = randint(50, 430)
#fonte e estilo
pontos = 0
font = pygame.font.SysFont("gabriola",38, True, True)

tela = pygame.display.set_mode((largura, altura)) #tamanho da tela do jogo
pygame.display.set_caption('jogo') #muda o nome da janela
relogio = pygame.time.Clock()

lista_cobra = []

comprimento_inicial = 5

morreu = False

def aumenta_cobra(lista_cobra):
    for XeY in lista_cobra:
        pygame.draw.rect(tela, (0, 255, 0), (XeY[0], XeY[1], 20, 20))

def reiniciar_jogo():
    global pontos, comprimento_inicial, x_cobra, y_cobra, lista_cobra, lista_cabeca, x_maca, y_maca, morreu
    pontos = 0
    comprimento_inicial = 5
    x_cobra = int(largura / 2)
    y_cobra = int(altura / 2)
    lista_cobra = []
    lista_cabeca = []
    x_maca = randint(40, 600)
    y_maca = randint(50, 430)
    morreu = False

while True: #roda o jogo em um lup
    relogio.tick(40)
    tela.fill((0, 0, 0))
    msg = f"pontos: {pontos}"
    testo_formatado = font.render(msg, True, (255,255,255))
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit() # fecha o jogo em kit

        #Movimento
        if event.type == KEYDOWN:
            if event.key == K_a:
                if x_controle == velocidade:
                    pass
                else:
                    x_controle =  - velocidade
                    y_controle = 0
            elif event.key == K_d:
                if x_controle == - velocidade:
                    pass
                else:
                    x_controle = velocidade
                    y_controle = 0
            elif event.key == K_w:
                if y_controle == velocidade:
                    pass
                else:
                    y_controle = - velocidade
                    x_controle = 0
            elif event.key == K_s:
                if y_controle == - velocidade:
                    pass
                else:
                    y_controle = velocidade
                    x_controle = 0

    x_cobra = x_cobra + x_controle  
    y_cobra = y_cobra + y_controle      

    #pygame.draw - cria um objeto
    cobra = pygame.draw.rect(tela, (0,255,0), (x_cobra,y_cobra, 20, 20))#cria um retangulo
    maca = pygame.draw.rect(tela, (255,0,0), (x_maca, y_maca, 20, 20))

    if cobra.colliderect(maca):
        x_maca = randint(40, 600)
        y_maca = randint(50, 430)
        pontos += 1
        colisao.play()
        comprimento_inicial = comprimento_inicial + 5

    lista_cabeca = []
    lista_cabeca.append(x_cobra)
    lista_cabeca.append(y_cobra)

    
    lista_cobra.append(lista_cabeca)

    if lista_cobra.count(lista_cabeca) > 1:
        font2 = pygame.font.SysFont('arial', 20, True, True)
        mensagem = 'GAME OVER - precione a tecla R para jogar novamente!'
        texto_formatado = font2.render(mensagem, True, (255,255,255))
        ret_texto = texto_formatado.get_rect()

        morreu = True
        while morreu:
            tela.fill((210,100,0))
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.QUIT() 
                    exit()
                
                if event.type == KEYDOWN:
                    if event.key == K_r:
                        reiniciar_jogo()
            
            ret_texto.center = (largura//2, altura//2)
            tela.blit(texto_formatado, ret_texto)
            pygame.display.update()    

    if x_cobra > largura:
        x_cobra = 0
    elif x_cobra < 0:
        x_cobra = largura
    elif y_cobra < 0:
        y_cobra = altura
    elif y_cobra > altura:
        y_cobra = 0
    

    if len(lista_cobra) > comprimento_inicial:
        del lista_cobra[0]

    aumenta_cobra(lista_cobra)

    tela.blit(testo_formatado, (415, 40))
    pygame.display.update() #Atualisa a pagina