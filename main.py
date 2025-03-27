
import pygame
import random
import sys

# Inicializando o pygame
pygame.init()

# Definindo as dimensões da tela
LARGURA = 800
ALTURA = 600
screen = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Jogo de Naves 2D")

# Definindo as cores
BRANCO = (255, 255, 255)
VERDE = (0, 255, 0)
VERMELHO = (255, 0, 0)
AZUL = (0, 0, 255)


# Definindo o relógio para controlar a taxa de quadros
clock = pygame.time.Clock()

# Definir o tamanho da nave e dos projéteis
TAM_NAVE = 50
TAM_PROJETIL = 5
VELOCIDADE_NAVE = 5
VELOCIDADE_PROJETIL = 7
VELOCIDADE_INIMIGO = 3
QUANTIDADE_INIMIGOS = 5

# Fonte para o texto
font = pygame.font.Font(None, 36)

# Classe para a nave do jogador
class Nave:
    def __init__(self):
        self.x = LARGURA // 2 - TAM_NAVE // 2
        self.y = ALTURA - TAM_NAVE - 10

        self.velocidade = VELOCIDADE_NAVE

    def mover(self, teclas):
        if teclas[pygame.K_LEFT] and self.x > 0:
            self.x -= self.velocidade
        if teclas[pygame.K_RIGHT] and self.x < LARGURA - TAM_NAVE:
            self.x += self.velocidade

    def desenhar(self):
        pygame.draw.rect(screen, AZUL, (self.x, self.y, TAM_NAVE, TAM_NAVE))

# Classe para os projéteis
class Projetil:
    def __init__(self, x, y):
        self.x = x + TAM_NAVE // 2 - TAM_PROJETIL // 2
        self.y = y
        self.velocidade = VELOCIDADE_PROJETIL

    def mover(self):
        self.y -= self.velocidade

    def desenhar(self):
        pygame.draw.rect(screen, VERDE, (self.x, self.y, TAM_PROJETIL, TAM_PROJETIL))

# Classe para os inimigos
class Inimigo:
    def __init__(self):
        self.x = random.randint(0, LARGURA - TAM_NAVE)
        self.y = random.randint(-150, -50)
        self.velocidade = VELOCIDADE_INIMIGO

    def mover(self):
        self.y += self.velocidade


    def desenhar(self):
        pygame.draw.rect(screen, VERMELHO, (self.x, self.y, TAM_NAVE, TAM_NAVE))

# Função para verificar colisões
def verificar_colisao(projetil, inimigo):
    if projetil.x > inimigo.x and projetil.x < inimigo.x + TAM_NAVE:
        if projetil.y > inimigo.y and projetil.y < inimigo.y + TAM_NAVE:
            return True
    return False

# Função para exibir a pontuação
def exibir_pontuacao(pontuacao):
    texto = font.render(f"Pontuação: {pontuacao}", True, BRANCO)
    screen.blit(texto, (10, 10))

# Função principal do jogo

def jogo():
    nave = Nave()
    inimigos = [Inimigo() for _ in range(QUANTIDADE_INIMIGOS)]
    projetis = []
    pontuacao = 0

    while True:
        screen.fill((0, 0, 0))  # Limpar a tela

        # Verificando eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    projetil = Projetil(nave.x, nave.y)
                    projetis.append(projetil)

        # Movimentação da nave
        teclas = pygame.key.get_pressed()
        nave.mover(teclas)

        # Movimentando e desenhando os projéteis
        for projetil in projetis[:]:
            projetil.mover()
            projetil.desenhar()
            # Remover projéteis que saem da tela
            if projetil.y < 0:
                projetis.remove(projetil)

        # Movimentando e desenhando os inimigos
        for inimigo in inimigos[:]:
            inimigo.mover()
            inimigo.desenhar()
            # Verificar se o inimigo saiu da tela
            if inimigo.y > ALTURA:

                inimigos.remove(inimigo)
                inimigos.append(Inimigo())  # Adicionar novo inimigo
            # Verificar colisão entre projétil e inimigo
            for projetil in projetis[:]:
                if verificar_colisao(projetil, inimigo):
                    projetis.remove(projetil)
                    inimigos.remove(inimigo)
                    inimigos.append(Inimigo())  # Adicionar novo inimigo
                    pontuacao += 1
                    break

        # Desenhar a nave do jogador
        nave.desenhar()

        # Exibir a pontuação
        exibir_pontuacao(pontuacao)

        # Atualizar a tela
        pygame.display.update()

        # Controlar a taxa de quadros por segundo
        clock.tick(60)

# Iniciar o jogo
jogo()