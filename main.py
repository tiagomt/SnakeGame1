from multiprocessing.sharedctypes import Value
from numpy import diff
import pygame
# variaveis locais para capturar eventos, como KEYDOWN
from pygame.locals import *
import time
import random

SIZE = 40
difficulty = 0.3


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

    def move(self):
        self.x = random.randint(0, 24)*SIZE
        self.y = random.randint(0, 19)*SIZE


class Snake:

    def __init__(self, parent_screen, length):

        self.parent_screen = parent_screen
        # carregando imagem "bloco"
        self.block = pygame.image.load("./resources/block.jpg").convert()
        # direção padrão
        self.direction = "down"

        self.length = length
        self.x = [SIZE]*length
        self.y = [SIZE]*length

    # aumenta o tamanho da snake e o array do tamanho
    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

    def draw(self):

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

        # modulo pygame para sons
        pygame.mixer.init()

        self.play_background_music()

        # definindo cor
        self.surface.fill((110, 110, 5))

        # definindo snake dentro do game passando a tela do game
        self.snake = Snake(self.surface, 1)

        # jogando block na tela do game
        self.snake.draw()

        # definindo apple dentro do game passando a tela do game
        self.apple = Apple(self.surface)

        # jogando apple na tela do game
        self.apple.draw()

    # logica snake comendo maçã
    def is_collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + SIZE:
            if y1 >= y2 and y1 < y2 + SIZE:
                return True
        return False

    def play_background_music(self):
        # mixer.music é para musicas longas
        pygame.mixer.music.load("./resources/bg_music_1.mp3")
        pygame.mixer.music.play()

    def play_sound(self, sound):
        # mixer.Sound a musica toca uma vez
        sound = pygame.mixer.Sound(f"./resources/{sound}.mp3")
        pygame.mixer.Sound.play(sound)

    def render_background(self):
        bg = pygame.image.load("./resources/background.jpg")
        self.surface.blit(bg, (0, 0))

    def play(self):
        self.render_background()
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()

        # colisao snake com apple
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):

            self.play_sound("ding")

            self.snake.increase_length()

            self.change_difficulty()

            self.apple.move()

        # colisao snake com ela propria
        for i in range(2, self.snake.length):

            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):

                self.play_sound("crash")

                # lançando erro para ser pego pelo try
                raise "Game over"

        # colisao com as bordas
        if not (0 <= self.snake.x[0] <= 1000 and 0 <= self.snake.y[0] <= 800):
            self.play_sound('crash')
            raise "Tocou nas bordas"

    # pontuação do jogo

    def display_score(self):
        font = pygame.font.SysFont('arial', 30)
        score = font.render(
            f"Score: {self.snake.length}", True, (255, 255, 255))
        self.surface.blit(score, (800, 10))

    # mensagem de game over
    def show_game_over(self):
        self.render_background()
        font = pygame.font.SysFont('arial', 30)

        line1 = font.render(
            f"Game is over! Sua pontuacao e {self.snake.length}", True, (255, 255, 255))
        self.surface.blit(line1, (200, 300))

        line2 = font.render(
            "Para jogar de novo, pressione Enter. Para sair, pressione ESC!", True, (255, 255, 255))
        self.surface.blit(line2, (200, 350))

        pygame.display.flip()

        # pause música de background
        pygame.mixer.music.pause()

    def change_difficulty(self):
        global difficulty
        if self.snake.length % 2 == 0:
            if difficulty - 0.05 <= 0:
                difficulty = 0.01
            else:
                difficulty -= 0.05

    def reset(self):

        self.snake = Snake(self.surface, 1)
        self.apple = Apple(self.surface)

    def run(self):
        running = True
        pause = False

        while running:
            # captura de eventos
            for event in pygame.event.get():

                if event.type == KEYDOWN:

                    # fechar janela no ESC
                    if event.key == K_ESCAPE:
                        running = False

                    if event.key == K_RETURN:
                        pygame.mixer.music.unpause()
                        pause = False

                    if not pause:
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

            try:
                if not pause:
                    self.play()
            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()

            time.sleep(difficulty)


if __name__ == "__main__":

    game = Game()
    game.run()
