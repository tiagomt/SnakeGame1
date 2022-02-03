import pygame
# import time
# variaveis locais para capturar eventos, como KEYDOWN
from pygame.locals import *

if __name__ == "__main__":
    pygame.init()

    # iniciando a janela do jogo com 500x500
    surface = pygame.display.set_mode((500, 500))

    # definindo cor
    surface.fill((110, 110, 5))

    # atualizando tela
    pygame.display.flip()

    # tempo ate fechar janela
    # time.sleep(5)

    running = True

    while running:
        # captura de eventos
        for event in pygame.event.get():

            if event.type == KEYDOWN:
                # fechar janela no ESC
                if event.key == K_ESCAPE:
                    running = False

            # fechar janela no X
            elif event.type == QUIT:
                running = False
