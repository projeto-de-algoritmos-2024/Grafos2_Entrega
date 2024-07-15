import pygame
from pygame.locals import *
from constantes import *
from main import main


pygame.init()

screen = pygame.display.set_mode((largura_tela, altura_tela))
font = pygame.font.SysFont('arial', 20, True, False)
res = 0

pygame.display.set_caption(titulo)


# Função para desenhar a grade
def desenha_mapa():
    casa = 1
    rua = 1
    for linha in range(linhas):
        for coluna in range(colunas):
            rect = pygame.Rect(coluna * tamanho_casa, linha * tamanho_casa, tamanho_casa, tamanho_casa)
            
            if mapa[linha][coluna] == 'rh':
                pygame.draw.rect(screen, CINZA_ESCURO, rect)
                formatado = font.render(f'{rua}', True, PRETO)
                rua += 1
                screen.blit(formatado, (coluna * tamanho_casa + 15, linha * tamanho_casa + 15))
                # pygame.draw.rect(screen, BRANCO, rect, 1)
            elif mapa[linha][coluna] == 'rv':
                pygame.draw.rect(screen, CINZA_ESCURO, rect)
                formatado = font.render(f'{rua}', True, PRETO)
                rua += 1
                screen.blit(formatado, (coluna * tamanho_casa + 15, linha * tamanho_casa + 15))
                # pygame.draw.rect(screen, BRANCO, rect, 1)
            elif mapa[linha][coluna] == farmacia:
                pygame.draw.rect(screen, VERMELHO, rect)
                pygame.draw.rect(screen, VERDE, rect, 5)
            else:
                pygame.draw.rect(screen, AZUL, rect)
                pygame.draw.rect(screen, VERDE, rect, 5)
                formatado = font.render(f'{mapa[linha][coluna]}', True, CINZA_ESCURO)
                casa += 1
                screen.blit(formatado, (coluna * tamanho_casa + 15, linha * tamanho_casa + 15))
            
def desenha_botao():
    rect = pygame.Rect(alinhamento_lateral, posicao_botao_buscar, largura_botao, altura_botao)
    pygame.draw.rect(screen, BRANCO, rect)
    pygame.draw.rect(screen, PRETO, rect, 3)


def exportar_json():
    casas_selecionadas = list()
    for i in range(len(selecionadas)):
        for j in range(len(selecionadas[0])):
            if selecionadas[i][j]:
                casas_selecionadas.append(int(mapa[i][j]))
    global res
    res = main([int(farmacia)] + casas_selecionadas)


def mostra_resultado():
    mensagem = f'Distância percorrida: {res[0]}'
    formatado2 = font.render(mensagem, True, PRETO)
    screen.blit(formatado2, (alinhamento_lateral + 10, posicao_botao_buscar + 100))
    mensagem = f'Caminho das ruas: {res[1]}'
    formatado2 = font.render(mensagem, True, PRETO)
    screen.blit(formatado2, (alinhamento_lateral + 10, posicao_botao_buscar + 140))

# Inicializa as casas como não selecionadas
selecionadas = [[False for _ in range(colunas)] for _ in range(linhas)]

# Loop principal
rodando = True
escolhendo = True
while rodando:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            coluna = x // tamanho_casa
            linha = y // tamanho_casa
            if (linha in (1,2,4,5) and coluna in (1,2,3,5,6,7,9,10,11,13,14,15)) and not (linha == 2 and coluna == 14):
                selecionadas[linha][coluna] = not selecionadas[linha][coluna]
            elif x >= alinhamento_lateral and x < (alinhamento_lateral + largura_botao):
                if y >= posicao_botao_buscar and y < (posicao_botao_buscar + altura_botao):
                    exportar_json()
                    escolhendo = False 

    screen.fill(AMBIENTE)
    desenha_mapa()

    # Desenha as casas selecionadas
    for linha in range(linhas):
        for coluna in range(colunas):
            if selecionadas[linha][coluna]:
                rect = pygame.Rect(coluna * tamanho_casa, linha * tamanho_casa, tamanho_casa, tamanho_casa)
                pygame.draw.rect(screen, BRANCO, rect)

    if escolhendo:
        mensagem = 'Selecione as casas desejadas:'
        formatado2 = font.render(mensagem, True, PRETO)
        screen.blit(formatado2, (alinhamento_lateral, 5))
        desenha_botao()
        mensagem = 'Buscar'
        formatado2 = font.render(mensagem, True, PRETO)
        screen.blit(formatado2, (alinhamento_lateral + 10, posicao_botao_buscar + 5))
    else:
        mostra_resultado()

    pygame.display.flip()

pygame.quit()
