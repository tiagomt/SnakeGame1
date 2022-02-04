import pygame
# import time
# variaveis locais para capturar eventos, como KEYDOWN
from pygame.locals import *


class Snake:

    def __init__(self, parent_screen):

        self.parent_screen = parent_screen
        # carregando imagem "bloco"
        self.block = pygame.image.load("./resources/block.jpg").convert()
        self.x = 100
        self.y = 100

    def draw(self):
        # self.parent_screen.fill irá "apagar" blocos anteriores
        self.parent_screen.fill((110, 110, 5))

        # joga block no parent_screen(tela do game)
        self.parent_screen.blit(self.block, (self.x, self.y))

        # atualizando tela
        pygame.display.flip()

    def move_left(self):
        self.x -= 10
        self.draw()

    def move_right(self):
        self.x += 10
        self.draw()

    def move_up(self):
        self.x -= 10
        self.draw()

    def move_down(self):
        self.x += 10
        self.draw()


class Game:
    def __init__(self):
        # inicializando pygame
        pygame.init()

        # iniciando a janela do jogo com 1000x500
        self.surface = pygame.display.set_mode((500, 500))

        # definindo cor
        self.surface.fill((110, 110, 5))

        # definindo snake dentro do game passando a tela do game
        self.snake = Snake(self.surface)

        # jogando block na tela do game
        self.snake.draw()

    def run(self):
        running = True

        while running:
            # captura de eventos
            for event in pygame.event.get():

                if event.type == KEYDOWN:

                    # fechar janela no ESC
                    if event.key == K_ESCAPE:
                        running = False

                    if event.key == K_UP:
                        self.snake.move_up()

                    if event.key == K_DOWN:
                        self.snake.move_down()

                    if event.key == K_LEFT:
                        self.snake.move_left()

                    if event.key == K_RIGHT:
                        self.snake.move_right()

                # fechar janela no X
                elif event.type == QUIT:
                    running = False


if __name__ == "__main__":

    game = Game()
    game.run()
