import logging

import pygame

from snake import Snake
from game import Game


class Engine:
    white = (255, 255, 255)
    black = (0, 0, 0)
    red = (255, 0, 0)
    green = (0, 255, 0)
    background = (204, 204, 255)
    # размер одного блока в пикселях
    block_size = 12
    speed = 7

    def __init__(self, game: Game, window_caption: str):
        pygame.init()
        self.game = game
        self.window_width = game.board.width * self.block_size
        self.window_height = game.board.height * self.block_size
        self.display = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption(window_caption)
        self.clock = pygame.time.Clock()
        logging.info(f'New game initialized: {window_caption}, {self.window_width}x{self.window_height}')

    def quit(self):
        pygame.quit()
        quit()

    def draw_frame(self):
        self.display.fill(self.background)

        # render snake
        for block in self.game.board.snake.blocks:
            pygame.draw.rect(self.display,
                             self.red if block.is_head else self.black,
                             [block.x * self.block_size,
                              block.y * self.block_size,
                              self.block_size, self.block_size])

        # render food
        pygame.draw.rect(self.display, self.green,
                         [self.game.board.food.x * self.block_size,
                          self.game.board.food.y * self.block_size,
                          self.block_size, self.block_size])

        # show score
        font_style = pygame.font.SysFont("bahnschrift", 25)
        score = font_style.render(f'Ваш счёт: {str(self.game.score)} '
                                  f'Длина питона: {len(self.game.board.snake.blocks)} '
                                  f'X:{self.game.board.snake.head.x}, Y{self.game.board.snake.head.y}',
                                  True, self.black)
        self.display.blit(score, [0, 0])

        pygame.display.update()
        self.clock.tick(self.speed)

    def game_loop(self):
        while not self.game.is_gameover:
            for event in pygame.event.get():
                # print(event)
                if event.type == pygame.QUIT:
                    self.game.game_over()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        self.game.board.snake.set_direction(Snake.direction_right)
                    elif event.key == pygame.K_DOWN:
                        self.game.board.snake.set_direction(Snake.direction_down)
                    elif event.key == pygame.K_LEFT:
                        self.game.board.snake.set_direction(Snake.direction_left)
                    elif event.key == pygame.K_UP:
                        self.game.board.snake.set_direction(Snake.direction_up)
                    elif event.key == pygame.K_SPACE:
                        self.game.toggle_pause()

            self.game.make_move()
            self.draw_frame()
