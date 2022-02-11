import pygame
# variaveis locais para capturar eventos, como KEYDOWN
from pygame.locals import *
import time

SIZE = 40


class Apple:
    def __init__(self, parent_screen):
        self.image = pygame.image.load("./resources/apple.jpg").convert()
        self.parent_screen = parent_screen
        self.x = SIZE * 3
        self.y = SIZE * 3

    def draw(self):
        # joga block no parent_screen(tela do game)
        self.parent_screen.blit(self.image, (self.x, self.y))

        # atualizando tela
        pygame.display.flip()


class Snake:

    def __init__(self, parent_screen, length):

        self.length = length
        self.parent_screen = parent_screen
        # carregando imagem "bloco"
        self.block = pygame.image.load("./resources/block.jpg").convert()
        self.x = [SIZE]*length
        self.y = [SIZE]*length
        # direção padrão
        self.direction = "down"

    def draw(self):
        # self.parent_screen.fill irá "apagar" blocos anteriores
        self.parent_screen.fill((110, 110, 5))

        # for para jogar blocos na tela
        for i in range(self.length):
            # joga block no parent_screen(tela do game)
            self.parent_screen.blit(self.block, (self.x[i], self.y[i]))

        # atualizando tela
        pygame.display.flip()

    def move_left(self):
        self.direction = "left"

    def move_right(self):
        self.direction = "right"

    def move_up(self):
        self.direction = "up"

    def move_down(self):
        self.direction = "down"

    def walk(self):

        # definindo posição do bloco como bloco anterior
        for i in range(self.length - 1, 0, -1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]

        # movimento do tamnanho do bloco(SIZE)
        if self.direction == "left":
            self.x[0] -= SIZE

        if self.direction == "right":
            self.x[0] += SIZE

        if self.direction == "up":
            self.y[0] -= SIZE

        if self.direction == "down":
            self.y[0] += SIZE

        self.draw()


class Game:
    def __init__(self):
        # inicializando pygame
        pygame.init()

        # iniciando a janela do jogo com 1000x500
        self.surface = pygame.display.set_mode((1000, 800))

        # definindo cor
        self.surface.fill((110, 110, 5))

        # definindo snake dentro do game passando a tela do game
        self.snake = Snake(self.surface, 6)

        # jogando block na tela do game
        self.snake.draw()

        # definindo apple dentro do game passando a tela do game
        self.apple = Apple(self.surface)

        # jogando apple na tela do game
        self.apple.draw()

    def play(self):
        self.snake.walk()
        self.apple.draw()

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

            self.play()
            time.sleep(0.3)


if __name__ == "__main__":

    game = Game()
    game.run()
