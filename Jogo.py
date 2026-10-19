import pygame
import math
import random

pygame.init()

LARGURA = 800
ALTURA = 600

TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("SquareGame")

# Cores
AZUL = (50, 120, 255)
VERMELHO = (220, 50, 50)
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
CINZA = (40, 40, 40)
VERDE = (50, 200, 100)

# Relógio para controlar o jogo
clock = pygame.time.Clock()

# Fonte
fonte = pygame.font.SysFont("Arial", 28)
fonte_grande = pygame.font.SysFont("Arial", 50)


# ==========================================
# JOGADOR
# ==========================================

TAMANHO_JOGADOR = 40

jogador = pygame.Rect(
    LARGURA // 2 - TAMANHO_JOGADOR // 2,
    ALTURA // 2 - TAMANHO_JOGADOR // 2,
    TAMANHO_JOGADOR,
    TAMANHO_JOGADOR
)

VELOCIDADE_JOGADOR = 5


# ==========================================
# INIMIGO
# ==========================================

TAMANHO_INIMIGO = 40

inimigo = pygame.Rect(
    random.randint(0, LARGURA - TAMANHO_INIMIGO),
    random.randint(0, ALTURA - TAMANHO_INIMIGO),
    TAMANHO_INIMIGO,
    TAMANHO_INIMIGO
)

VELOCIDADE_INIMIGO = 2


# ==========================================
# PONTUAÇÃO
# ==========================================

pontuacao = 0

# A pontuação aumenta com o tempo
tempo_pontuacao = 0


# ==========================================
# FUNÇÃO PARA REINICIAR O JOGO
# ==========================================

def reiniciar_jogo():
    global pontuacao
    global VELOCIDADE_INIMIGO
    global tempo_pontuacao

    jogador.x = LARGURA // 2 - TAMANHO_JOGADOR // 2
    jogador.y = ALTURA // 2 - TAMANHO_JOGADOR // 2

    inimigo.x = random.randint(0, LARGURA - TAMANHO_INIMIGO)
    inimigo.y = random.randint(0, ALTURA - TAMANHO_INIMIGO)

    pontuacao = 0
    tempo_pontuacao = 0
    VELOCIDADE_INIMIGO = 2


# ==========================================
# TELA DE GAME OVER
# ==========================================

def tela_game_over():

    while True:

        TELA.fill(PRETO)

        texto = fonte_grande.render("GAME OVER", True, VERMELHO)
        TELA.blit(
            texto,
            (
                LARGURA // 2 - texto.get_width() // 2,
                180
            )
        )

        texto_pontos = fonte.render(
            f"Pontuação: {pontuacao}",
            True,
            BRANCO
        )

        TELA.blit(
            texto_pontos,
            (
                LARGURA // 2 - texto_pontos.get_width() // 2,
                260
            )
        )

        texto_reiniciar = fonte.render(
            "Pressione R para jogar novamente",
            True,
            BRANCO
        )

        TELA.blit(
            texto_reiniciar,
            (
                LARGURA // 2 - texto_reiniciar.get_width() // 2,
                330
            )
        )

        texto_sair = fonte.render(
            "Pressione ESC para sair",
            True,
            BRANCO
        )

        TELA.blit(
            texto_sair,
            (
                LARGURA // 2 - texto_sair.get_width() // 2,
                380
            )
        )

        pygame.display.update()

        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:
                return False

            if evento.type == pygame.KEYDOWN:

                if evento.key == pygame.K_r:
                    reiniciar_jogo()
                    return True

                if evento.key == pygame.K_ESCAPE:
                    return False


# ==========================================
# LOOP PRINCIPAL
# ==========================================

rodando = True

while rodando:

    # Controla a velocidade do jogo
    clock.tick(60)

    # ======================================
    # EVENTOS
    # ======================================

    for evento in pygame.event.get():

        if evento.type == pygame.QUIT:
            rodando = False

        # ESC fecha o jogo
        if evento.type == pygame.KEYDOWN:

            if evento.key == pygame.K_ESCAPE:
                rodando = False


    # ======================================
    # MOVIMENTAÇÃO DO JOGADOR
    # ======================================

    teclas = pygame.key.get_pressed()

    if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
        jogador.x -= VELOCIDADE_JOGADOR

    if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
        jogador.x += VELOCIDADE_JOGADOR

    if teclas[pygame.K_UP] or teclas[pygame.K_w]:
        jogador.y -= VELOCIDADE_JOGADOR

    if teclas[pygame.K_DOWN] or teclas[pygame.K_s]:
        jogador.y += VELOCIDADE_JOGADOR


    # ======================================
    # IMPEDIR O JOGADOR DE SAIR DA TELA
    # ======================================

    if jogador.left < 0:
        jogador.left = 0

    if jogador.right > LARGURA:
        jogador.right = LARGURA

    if jogador.top < 0:
        jogador.top = 0

    if jogador.bottom > ALTURA:
        jogador.bottom = ALTURA


    # ======================================
    # INIMIGO PERSEGUINDO O JOGADOR
    # ======================================

    diferenca_x = jogador.centerx - inimigo.centerx
    diferenca_y = jogador.centery - inimigo.centery

    distancia = math.sqrt(
        diferenca_x ** 2 + diferenca_y ** 2
    )

    if distancia != 0:

        movimento_x = diferenca_x / distancia
        movimento_y = diferenca_y / distancia

        inimigo.x += int(movimento_x * VELOCIDADE_INIMIGO)
        inimigo.y += int(movimento_y * VELOCIDADE_INIMIGO)


    # ======================================
    # MELHORIA:
    # INIMIGO FICA MAIS RÁPIDO COM O TEMPO
    # ======================================

    tempo_pontuacao += 1

    if tempo_pontuacao >= 60:

        pontuacao += 1
        tempo_pontuacao = 0

        # A cada 5 pontos o inimigo fica mais rápido
        if pontuacao % 5 == 0:

            VELOCIDADE_INIMIGO += 0.5


    # ======================================
    # COLISÃO
    # ======================================

    if jogador.colliderect(inimigo):

        continuar = tela_game_over()

        if continuar:

            continue

        else:

            rodando = False


    # ======================================
    # DESENHAR A TELA
    # ======================================

    TELA.fill(CINZA)

    # Desenha o jogador
    pygame.draw.rect(
        TELA,
        AZUL,
        jogador
    )

    # Desenha o inimigo
    pygame.draw.rect(
        TELA,
        VERMELHO,
        inimigo
    )


    # ======================================
    # EXIBIR PONTUAÇÃO
    # ======================================

    texto_pontuacao = fonte.render(
        f"Pontuação: {pontuacao}",
        True,
        BRANCO
    )

    TELA.blit(
        texto_pontuacao,
        (20, 20)
    )


    # ======================================
    # INSTRUÇÕES
    # ======================================

    instrucoes = fonte.render(
        "Use WASD ou as setas para se movimentar",
        True,
        BRANCO
    )

    TELA.blit(
        instrucoes,
        (
            LARGURA // 2 - instrucoes.get_width() // 2,
            ALTURA - 45
        )
    )


    # Atualiza a tela
    pygame.display.update()


# ==========================================
# ENCERRAR PYGAME
# ==========================================

pygame.quit()