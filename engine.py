import pygame

from game import Game
from snake import Snake


class Engine:
    white = (255, 255, 255)
    black = (0, 0, 0)
    red = (255, 0, 0)
    # размер одного блока в пикселях
    block_size = 10
    speed = 7

    def __init__(self, window_width: int, window_height: int, window_caption: str):
        pygame.init()
        self.window_width = window_width
        self.window_height = window_height
        self.display = pygame.display.set_mode((window_width, window_height))
        pygame.display.set_caption(window_caption)
        self.clock = pygame.time.Clock()

    def quit(self):
        pygame.quit()
        quit()

    def update(self, game):
        self.display.fill(self.white)

        for block in game.snake.blocks:
            pygame.draw.rect(self.display,
                             self.red if block.is_head else self.black,
                             [block.x * self.block_size,
                              self.window_height - block.y * self.block_size,
                              self.block_size, self.block_size])

        pygame.display.update()
        self.clock.tick(self.speed)

    def game_loop(self, game):
        while not game.is_gameover:
            for event in pygame.event.get():
                print(event)
                if event.type == pygame.QUIT:
                    game.game_over()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        game.snake.set_direction(Snake.direction_right)
                    elif event.key == pygame.K_DOWN:
                        game.snake.set_direction(Snake.direction_down)
                    elif event.key == pygame.K_LEFT:
                        game.snake.set_direction(Snake.direction_left)
                    elif event.key == pygame.K_UP:
                        game.snake.set_direction(Snake.direction_up)

            game.snake.make_move()
            self.update(game)

